"""
FinSight AI — ML Inference Module.

Loads trained models from disk and provides prediction functions
for the FastAPI prediction endpoints.
"""

import logging
from pathlib import Path
from typing import Optional

import joblib
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "models"

# ── Model Cache ───────────────────────────────────────────────
_model_cache: dict = {}


def _load_model(name: str) -> dict:
    """Load a model bundle from disk with caching."""
    if name not in _model_cache:
        path = MODELS_DIR / f"{name}.pkl"
        if not path.exists():
            raise FileNotFoundError(f"Model not found: {path}")
        _model_cache[name] = joblib.load(path)
        logger.info("Loaded model: %s", name)
    return _model_cache[name]


def predict_churn(features: dict) -> dict:
    """Predict churn probability for a single customer.

    Args:
        features: Dict with customer feature values

    Returns:
        Dict with churn_probability, risk_label, health_score
    """
    bundle = _load_model("churn_model")
    model = bundle["model"]
    feature_cols = bundle["feature_cols"]
    label_encoders = bundle["label_encoders"]
    categorical_features = bundle["categorical_features"]

    # Encode categoricals
    row = {}
    for col in feature_cols:
        val = features.get(col, 0)
        if col in categorical_features and col in label_encoders:
            le = label_encoders[col]
            try:
                val = le.transform([str(val)])[0]
            except ValueError:
                val = 0
        row[col] = val

    X = pd.DataFrame([row], columns=feature_cols)
    prob = float(model.predict_proba(X)[0][1])

    if prob >= 0.7:
        risk_label = "High Risk"
    elif prob >= 0.3:
        risk_label = "Medium Risk"
    else:
        risk_label = "Low Risk"

    return {
        "churn_probability": round(prob, 4),
        "risk_label": risk_label,
        "health_score": round((1 - prob) * 100, 2),
    }


def predict_campaign(features: dict) -> dict:
    """Predict campaign conversion probability.

    Args:
        features: Dict with campaign feature values

    Returns:
        Dict with conversion_probability and recommendation
    """
    bundle = _load_model("campaign_model")
    model = bundle["model"]
    feature_cols = bundle["feature_cols"]
    label_encoders = bundle.get("label_encoders", {})
    categorical_cols = bundle.get("categorical_cols", [])

    row = {}
    for col in feature_cols:
        val = features.get(col, 0)
        if col in categorical_cols and col in label_encoders:
            le = label_encoders[col]
            try:
                val = le.transform([str(val)])[0]
            except ValueError:
                val = 0
        row[col] = val

    X = pd.DataFrame([row], columns=feature_cols)
    prob = float(model.predict_proba(X)[0][1])

    return {
        "conversion_probability": round(prob, 4),
        "recommendation": "Target" if prob >= 0.5 else "Skip",
    }


def predict_compliance(features: dict) -> dict:
    """Predict KYC compliance risk tier.

    Args:
        features: Dict with KYC risk flag values

    Returns:
        Dict with risk_tier and risk_score
    """
    bundle = _load_model("compliance_model")
    model = bundle["model"]
    feature_cols = bundle["feature_cols"]
    sector_encoder = bundle.get("sector_risk_encoder")

    row = {}
    for col in feature_cols:
        val = features.get(col, 0)
        if col == "sector_risk_encoded" and sector_encoder:
            sector_val = features.get("sector_risk", "Low")
            try:
                val = sector_encoder.transform([sector_val])[0]
            except ValueError:
                val = 0
        row[col] = val

    X = pd.DataFrame([row], columns=feature_cols)
    pred_class = int(model.predict(X)[0])
    tier_map = {0: "Critical", 1: "High", 2: "Low", 3: "Medium"}
    risk_tier = tier_map.get(pred_class, "Unknown")

    proba = model.predict_proba(X)[0]
    risk_score = round(float(max(proba)), 4)

    return {
        "risk_tier": risk_tier,
        "risk_score": risk_score,
        "predicted_class": pred_class,
    }
