from pathlib import Path
import joblib, pandas as pd
from dotenv import load_dotenv; load_dotenv()

MODEL_PATH   = Path("models/churn/xgboost_model.pkl")
PROFILE_PATH = Path("data/processed/unified_customer_profile.csv")
CHURN_PATH   = Path("data/processed/churn_predictions.csv")

FEATURE_ORDER = [
    'Customer_Age', 'Dependent_count', 'Months_on_book',
    'Months_Inactive_12_mon', 'Contacts_Count_12_mon',
    'Credit_Limit', 'Total_Revolving_Bal', 'Avg_Open_To_Buy',
    'Total_Amt_Chng_Q4_Q1', 'Total_Trans_Amt', 'Total_Trans_Ct',
    'Total_Ct_Chng_Q4_Q1', 'Avg_Utilization_Ratio',
    'Income_Category', 'Card_Category', 'Gender',
    'Education_Level', 'Marital_Status'
]

def load_churn_model():
    """Load trained XGBoost churn prediction model from disk."""
    model = joblib.load(MODEL_PATH)
    try: model.get_booster().feature_names = None
    except: pass
    return model

def predict_churn(features: dict) -> dict:
    """Predict churn probability and risk label for a customer feature dict."""
    model = load_churn_model()
    X = pd.DataFrame([[features.get(k, 0) for k in FEATURE_ORDER]], columns=FEATURE_ORDER)
    prob = float(model.predict_proba(X)[0][1])
    label = "High Risk" if prob >= 0.7 else "Medium Risk" if prob >= 0.4 else "Loyal"
    return {"churn_probability": prob, "risk_label": label}

def get_churn_distribution() -> dict:
    """Return {risk_label: count} from unified profile churn_risk_label column."""
    df = pd.read_csv(PROFILE_PATH)
    return df['churn_risk_label'].value_counts().to_dict()

def get_top_churn_customers(n: int = 50) -> list:
    """Return top n customers by churn_probability as list of dicts."""
    df = pd.read_csv(PROFILE_PATH)
    cols = ['CLIENTNUM', 'churn_probability', 'churn_risk_label', 'segment_name']
    return df[cols].sort_values('churn_probability', ascending=False).head(n).to_dict(orient='records')
