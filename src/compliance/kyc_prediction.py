from pathlib import Path
import joblib, pandas as pd
from dotenv import load_dotenv; load_dotenv()

MODEL_PATH    = Path("models/kyc/xgboost_kyc.pkl")
PROCESSED_PATH = Path("data/processed/kyc_with_risk.csv")

SECTOR_MAP = {'Low': 0, 'Medium': 1, 'High': 2}

def load_kyc_model():
    """Load trained XGBoost KYC risk model from disk."""
    model = joblib.load(MODEL_PATH)
    try: model.get_booster().feature_names = None
    except: pass
    return model

def predict_kyc_risk(features: dict) -> dict:
    """Predict KYC risk score, level, and recommended action."""
    model = load_kyc_model()
    features['sector_risk'] = SECTOR_MAP.get(features.get('sector_risk', 'Low'), 0)
    X = pd.DataFrame([features])
    prob = float(model.predict_proba(X)[0][1])
    
    if prob > 0.75:
        level = "Critical"
        action = "Immediate account freeze and compliance review required"
    elif prob > 0.50:
        level = "High Risk"
        action = "Enhanced due diligence required immediately"
    elif prob > 0.25:
        level = "Medium Risk"
        action = "Schedule periodic review within 30 days"
    else:
        level = "Low Risk"
        action = "Standard monitoring — no immediate action required"
        
    return {"risk_score": round(prob, 4), "risk_level": level, "recommended_action": action}

def get_risk_distribution() -> dict:
    """Return {risk_level: count} from kyc_with_risk.csv."""
    df = pd.read_csv(PROCESSED_PATH)
    if 'risk_level' not in df.columns:
        df['risk_level'] = df['risk_score'].apply(lambda x: "Critical" if x > 0.75 else "High Risk" if x > 0.50 else "Medium Risk" if x > 0.25 else "Low Risk")
    return df['risk_level'].value_counts().to_dict()

def get_high_risk_customers(n: int = 50) -> list:
    """Return top n clients sorted by risk_score descending."""
    df = pd.read_csv(PROCESSED_PATH)
    cols = ['client_id', 'client_type', 'country', 'sector', 'pep_flag', 'sanctions_flag', 'risk_score', 'risk_level', 'recommended_action']
    available = [c for c in cols if c in df.columns]
    return df[available].sort_values('risk_score', ascending=False).head(n).to_dict(orient='records')
