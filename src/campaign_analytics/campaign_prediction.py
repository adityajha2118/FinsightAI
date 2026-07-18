from pathlib import Path
import joblib, pandas as pd
from dotenv import load_dotenv; load_dotenv()

MODEL_PATH = Path("models/campaign/xgboost_campaign.pkl")

def load_campaign_model():
    """Load trained XGBoost campaign conversion model from disk."""
    model = joblib.load(MODEL_PATH)
    try: model.get_booster().feature_names = None
    except: pass
    return model

def predict_campaign_success(features: dict) -> dict:
    """Predict conversion probability. Return {conversion_probability: float}."""
    try:
        model = load_campaign_model()
        X = pd.DataFrame([features])
        prob = float(model.predict_proba(X)[0][1]) if hasattr(model, "predict_proba") else float(model.predict(X)[0])
        return {"conversion_probability": prob}
    except Exception as e:
        return {"conversion_probability": 0.5, "error": str(e)}
