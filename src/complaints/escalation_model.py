from pathlib import Path
import joblib, pandas as pd

MODEL_PATH = Path("models/escalation/xgboost_escalation.pkl")

CATEGORY_MAP = {
    "Billing": 0, "Card Declined": 1, "Collections": 2,
    "Credit Reporting": 3, "Customer Service": 4,
    "Fraud": 5, "Rewards": 6, "Service Delay": 7, "Unknown": 8
}
EMOTION_MAP = {
    "Anger": 0, "Distress": 1, "Frustration": 2,
    "Legal Threat": 3, "Neutral": 4
}

def load_escalation_model():
    """Load trained XGBoost escalation prediction model from disk."""
    model = joblib.load(MODEL_PATH)
    try: model.get_booster().feature_names = None
    except: pass
    return model

def encode_for_escalation(category: str, emotion: str, narrative_length: int) -> dict:
    """Convert raw category/emotion strings to encoded feature dict for predict_escalation."""
    return {
        'category_encoded': CATEGORY_MAP.get(category, 8),
        'emotion_encoded': EMOTION_MAP.get(emotion, 4),
        'product_encoded': 0,
        'via_encoded': 0,
        'timely_binary': 0,
        'narrative_length': narrative_length
    }

def predict_escalation(features: dict) -> dict:
    """Predict escalation probability from feature dict."""
    try:
        model = load_escalation_model()
        feature_cols = ['category_encoded', 'emotion_encoded', 'product_encoded',
                        'via_encoded', 'timely_binary', 'narrative_length']
        X = pd.DataFrame([[features.get(k, 0) for k in feature_cols]], columns=feature_cols)
        prob = float(model.predict_proba(X)[0][1])
        return {"escalation_probability": round(prob, 4)}
    except Exception as e:
        return {"escalation_probability": 0.0}
