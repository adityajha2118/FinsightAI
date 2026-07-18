from pathlib import Path
import joblib, pandas as pd, numpy as np
from dotenv import load_dotenv; load_dotenv()

SCALER_PATH  = Path("models/segmentation/scaler.pkl")
MODEL_PATH   = Path("models/segmentation/kmeans_model.pkl")
PROFILE_PATH = Path("data/processed/unified_customer_profile.csv")
FEATURES_PATH = Path("data/feature_store/customer_features.parquet")

FEATURE_ORDER = ['Credit_Limit', 'Total_Trans_Amt', 'Total_Trans_Ct',
                 'Avg_Utilization_Ratio', 'Total_Revolving_Bal',
                 'Months_Inactive_12_mon']

def load_segmentation_model():
    """Load KMeans model and scaler from disk, return (scaler, model) tuple."""
    scaler = joblib.load(SCALER_PATH)
    model  = joblib.load(MODEL_PATH)
    return scaler, model

def predict_segment(features: dict) -> str:
    """Predict segment name for a customer."""
    scaler, model = load_segmentation_model()
    X = pd.DataFrame([[features.get(k, 0) for k in FEATURE_ORDER]], columns=FEATURE_ORDER)
    X_scaled = scaler.transform(X)
    cluster_id = int(model.predict(X_scaled)[0])
    if hasattr(model, 'cluster_map_'):
        return model.cluster_map_.get(cluster_id, f"Cluster {cluster_id}")
    # fallback: read from profile and get most common segment for that cluster
    df = pd.read_csv(PROFILE_PATH)
    if 'cluster_id' in df.columns and 'segment_name' in df.columns:
        mapping = df.groupby('cluster_id')['segment_name'].agg(lambda x: x.mode()[0])
        return mapping.get(cluster_id, f"Cluster {cluster_id}")
    return f"Cluster {cluster_id}"

def get_segment_distribution() -> dict:
    """Return {segment_name: count} from unified customer profile."""
    df = pd.read_csv(PROFILE_PATH)
    return df['segment_name'].value_counts().to_dict()

def get_segment_profiles() -> list:
    """Return mean feature values per segment as list of dicts for frontend table."""
    df = pd.read_csv(PROFILE_PATH)
    numeric_cols = ['Credit_Limit', 'Total_Trans_Amt', 'Total_Trans_Ct',
                    'Avg_Utilization_Ratio', 'Months_Inactive_12_mon',
                    'churn_probability', 'activity_score']
    available = [c for c in numeric_cols if c in df.columns]
    if 'segment_name' not in df.columns:
        return []
    return df.groupby('segment_name')[available].mean().round(4).reset_index().to_dict(orient='records')
