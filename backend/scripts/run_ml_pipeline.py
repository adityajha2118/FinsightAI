"""
FinSight AI — ML Training Pipeline.

Trains all 4 ML models and saves artifacts to backend/models/:
    1. Customer Churn (XGBoost)
    2. Customer Segmentation (K-Means)
    3. Campaign Response (XGBoost + SMOTE)
    4. Compliance Risk (XGBoost)

Each model reads from PostgreSQL, trains, evaluates, and serializes.

Usage:
    cd FinSight-AI/backend
    python -m scripts.run_ml_pipeline
"""

import logging
import sys
from pathlib import Path

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (
    classification_report, roc_auc_score, silhouette_score,
)
from sklearn.cluster import KMeans
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.database.engine import get_engine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)


# ═════════════════════════════════════════════════════════════
# 1. CHURN PREDICTION
# ═════════════════════════════════════════════════════════════

def train_churn_model():
    """Train XGBoost churn classifier.

    Business: Identifies customers likely to close their accounts.
    A probability score (0-1) enables the retention team to
    intervene at the right threshold (e.g., offer waived fees at 0.7+).
    """
    logger.info("=" * 50)
    logger.info("Training Churn Prediction Model (XGBoost)")
    logger.info("=" * 50)

    engine = get_engine()
    df = pd.read_sql("SELECT * FROM customers", engine)
    logger.info("Dataset: %d rows", len(df))

    # Target: binary churn flag
    df["is_churned"] = (df["attrition_flag"] == "Attrited Customer").astype(int)

    # Features
    numeric_features = [
        "customer_age", "dependent_count", "months_on_book",
        "months_inactive_12_mon", "contacts_count_12_mon",
        "credit_limit", "total_revolving_bal", "avg_open_to_buy",
        "total_amt_chng_q4_q1", "total_trans_amt", "total_trans_ct",
        "total_ct_chng_q4_q1", "avg_utilization_ratio",
    ]
    categorical_features = [
        "income_category", "card_category", "gender",
        "education_level", "marital_status",
    ]

    # Encode categoricals
    label_encoders = {}
    for col in categorical_features:
        le = LabelEncoder()
        df[col] = df[col].fillna("Unknown")
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    feature_cols = numeric_features + categorical_features
    X = df[feature_cols].fillna(0)
    y = df["is_churned"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="logloss",
        use_label_encoder=False,
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_prob)
    logger.info("ROC-AUC: %.4f", auc)
    logger.info("\n%s", classification_report(y_test, y_pred))

    # Save model + encoders + feature list
    save_path = MODELS_DIR / "churn_model.pkl"
    joblib.dump({
        "model": model,
        "label_encoders": label_encoders,
        "feature_cols": feature_cols,
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
    }, save_path)
    logger.info("✓ Saved to %s", save_path)

    # Generate predictions for all customers → customer_predictions table
    all_probs = model.predict_proba(X)[:, 1]
    predictions_df = pd.DataFrame({
        "client_id": df["client_id"],
        "churn_probability": np.round(all_probs, 4),
        "risk_label": pd.cut(
            all_probs,
            bins=[-0.01, 0.3, 0.7, 1.01],
            labels=["Low Risk", "Medium Risk", "High Risk"],
        ).astype(str),
        "health_score": np.round((1 - all_probs) * 100, 2),
        "activity_score": np.round(
            1 - (df["months_inactive_12_mon"].fillna(0) / 6).clip(0, 1), 4
        ),
    })
    predictions_df.to_sql("customer_predictions", engine, if_exists="append", index=False, method="multi")
    logger.info("✓ Customer predictions written to PostgreSQL (%d rows)", len(predictions_df))

    return auc


# ═════════════════════════════════════════════════════════════
# 2. CUSTOMER SEGMENTATION
# ═════════════════════════════════════════════════════════════

def train_segmentation_model():
    """Train K-Means clustering for customer segmentation.

    Business: Groups customers into behaviorally distinct segments
    so marketing can tailor offers (e.g., cashback for daily spenders,
    travel rewards for premium customers).
    """
    logger.info("=" * 50)
    logger.info("Training Customer Segmentation Model (K-Means)")
    logger.info("=" * 50)

    engine = get_engine()
    df = pd.read_sql("SELECT * FROM customers", engine)

    features = [
        "credit_limit", "total_trans_amt", "total_trans_ct",
        "avg_utilization_ratio", "total_revolving_bal",
        "months_inactive_12_mon",
    ]
    X = df[features].fillna(0)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    k = 5
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    model.fit(X_scaled)
    labels = model.labels_

    sil_score = silhouette_score(X_scaled, labels)
    logger.info("Silhouette Score: %.4f", sil_score)

    # Name segments based on centroid analysis
    df["cluster"] = labels
    centroids = df.groupby("cluster")[features].mean()

    segment_names = {}
    # Sort by credit_limit to assign meaningful names
    sorted_clusters = centroids.sort_values("credit_limit", ascending=False).index.tolist()
    name_map = {
        0: "Premium Customers",
        1: "Active Transactors",
        2: "Moderate Users",
        3: "Low Engagement",
        4: "At-Risk Dormant",
    }
    for rank, cluster_id in enumerate(sorted_clusters):
        segment_names[cluster_id] = name_map.get(rank, f"Segment {rank + 1}")

    # Save
    save_path = MODELS_DIR / "segmentation_model.pkl"
    joblib.dump({
        "model": model,
        "scaler": scaler,
        "features": features,
        "segment_names": segment_names,
    }, save_path)
    logger.info("✓ Saved to %s", save_path)

    # Write segment assignments to PostgreSQL
    segments_df = pd.DataFrame({
        "client_id": df["client_id"],
        "cluster_id": labels,
        "segment_name": [segment_names[c] for c in labels],
    })
    segments_df.to_sql("customer_segments", engine, if_exists="append", index=False, method="multi")
    logger.info("✓ Customer segments written to PostgreSQL (%d rows)", len(segments_df))

    return sil_score


# ═════════════════════════════════════════════════════════════
# 3. CAMPAIGN RESPONSE PREDICTION
# ═════════════════════════════════════════════════════════════

def train_campaign_model():
    """Train XGBoost campaign conversion predictor with SMOTE.

    Business: Predicts which customers are likely to subscribe
    to a term deposit, optimizing marketing spend by targeting
    high-propensity customers and avoiding fatigue on unlikely converters.
    """
    logger.info("=" * 50)
    logger.info("Training Campaign Model (XGBoost + SMOTE)")
    logger.info("=" * 50)

    engine = get_engine()
    df = pd.read_sql("SELECT * FROM campaigns", engine)
    logger.info("Dataset: %d rows", len(df))

    # Target
    df["converted"] = (df["subscribed"] == "yes").astype(int)

    # Encode categoricals
    categorical_cols = ["job", "marital", "education", "default_credit",
                        "housing", "loan", "contact", "month",
                        "day_of_week", "poutcome"]
    label_encoders = {}
    for col in categorical_cols:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = df[col].fillna("unknown")
            df[col] = le.fit_transform(df[col].astype(str))
            label_encoders[col] = le

    numeric_cols = ["age", "duration", "campaign_count", "pdays", "previous",
                    "emp_var_rate", "cons_price_idx", "cons_conf_idx",
                    "euribor3m", "nr_employed"]

    feature_cols = [c for c in numeric_cols + categorical_cols if c in df.columns]
    X = df[feature_cols].fillna(0)
    y = df["converted"]

    # SMOTE for class imbalance
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    min_samples = y_train.value_counts().min()
    if min_samples > 1:
        k_neighbors = min(5, min_samples - 1)
        smote = SMOTE(random_state=42, k_neighbors=k_neighbors)
        X_train_bal, y_train_bal = smote.fit_resample(X_train, y_train)
        logger.info("After SMOTE (k=%d): %d rows (was %d)", k_neighbors, len(X_train_bal), len(X_train))
    else:
        X_train_bal, y_train_bal = X_train, y_train
        logger.warning("Skipping SMOTE due to insufficient minority samples (%d)", min_samples)

    model = XGBClassifier(
        n_estimators=150,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        eval_metric="logloss",
        use_label_encoder=False,
    )
    model.fit(X_train_bal, y_train_bal)

    y_prob = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_prob)
    logger.info("ROC-AUC: %.4f", auc)

    # Save
    save_path = MODELS_DIR / "campaign_model.pkl"
    joblib.dump({
        "model": model,
        "label_encoders": label_encoders,
        "feature_cols": feature_cols,
        "numeric_cols": numeric_cols,
        "categorical_cols": categorical_cols,
    }, save_path)
    logger.info("✓ Saved to %s", save_path)

    return auc


# ═════════════════════════════════════════════════════════════
# 4. COMPLIANCE RISK CLASSIFICATION
# ═════════════════════════════════════════════════════════════

def train_compliance_model():
    """Train compliance risk classifier.

    Business: Automates KYC risk tier assignment based on
    transaction patterns, PEP status, sanctions matches,
    and entity opacity. Reduces manual compliance review burden.
    """
    logger.info("=" * 50)
    logger.info("Training Compliance Risk Model (XGBoost)")
    logger.info("=" * 50)

    engine = get_engine()
    df = pd.read_sql("SELECT * FROM kyc_profiles", engine)
    logger.info("Dataset: %d rows", len(df))

    # Create composite risk score as target
    risk_flags = [
        "pep_flag", "sanctions_flag", "ofac_country_flag",
        "structuring_pattern_flag", "rapid_movement_flag",
        "trade_mispricing_flag",
    ]
    available_flags = [c for c in risk_flags if c in df.columns]
    df["total_flags"] = df[available_flags].sum(axis=1)

    # Risk tiers based on flag count
    df["risk_tier"] = pd.cut(
        df["total_flags"],
        bins=[-1, 0, 1, 2, 100],
        labels=["Low", "Medium", "High", "Critical"],
    )

    # Encode sector_risk
    if "sector_risk" in df.columns:
        le_sector = LabelEncoder()
        df["sector_risk_encoded"] = le_sector.fit_transform(df["sector_risk"].fillna("Unknown"))
    else:
        le_sector = None

    feature_cols = available_flags + ["ownership_opacity_score"]
    if "sector_risk_encoded" in df.columns:
        feature_cols.append("sector_risk_encoded")
    if "transaction_count" in df.columns:
        feature_cols.append("transaction_count")

    X = df[feature_cols].fillna(0)
    y = LabelEncoder().fit_transform(df["risk_tier"])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        random_state=42,
        eval_metric="mlogloss",
        use_label_encoder=False,
    )
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    logger.info("Accuracy: %.4f", accuracy)

    # Save
    save_path = MODELS_DIR / "compliance_model.pkl"
    joblib.dump({
        "model": model,
        "feature_cols": feature_cols,
        "risk_flags": available_flags,
        "sector_risk_encoder": le_sector,
    }, save_path)
    logger.info("✓ Saved to %s", save_path)

    return accuracy


# ═════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════

def run_all():
    """Train all models sequentially."""
    logger.info("=" * 60)
    logger.info("FinSight AI — ML Training Pipeline")
    logger.info("=" * 60)

    results = {}
    results["churn_auc"] = train_churn_model()
    results["segmentation_silhouette"] = train_segmentation_model()
    results["campaign_auc"] = train_campaign_model()
    results["compliance_accuracy"] = train_compliance_model()

    logger.info("=" * 60)
    logger.info("Training Complete!")
    for metric, value in results.items():
        logger.info("  %s: %.4f", metric, value)
    logger.info("=" * 60)


if __name__ == "__main__":
    run_all()
