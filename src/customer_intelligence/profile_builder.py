from pathlib import Path
import pandas as pd
from dotenv import load_dotenv; load_dotenv()

PROFILE_PATH = Path("data/processed/unified_customer_profile.csv")

def get_unified_profile(client_id: str) -> dict:
    """Return unified profile row for CLIENTNUM as dict. Return error dict if not found."""
    df = pd.read_csv(PROFILE_PATH)
    df['CLIENTNUM'] = df['CLIENTNUM'].astype(str)
    row = df[df['CLIENTNUM'] == str(client_id)]
    if row.empty:
        return {"error": f"Client {client_id} not found"}
    return row.iloc[0].to_dict()

def get_executive_kpis() -> dict:
    """Return executive KPIs dict."""
    df = pd.read_csv(PROFILE_PATH)
    total = len(df)
    if total == 0:
        return {"total_customers": 0, "churn_rate": 0, "high_risk_count": 0, "active_rate": 0, "avg_credit_limit": 0}
        
    if 'segment_name' not in df.columns:
        df['segment_name'] = 'Unknown'
        
    high_risk = (df['churn_risk_label'] == 'High Risk').sum() if 'churn_risk_label' in df.columns else 0
    active = (df['activity_category'] == 'Active').sum() if 'activity_category' in df.columns else 0
    return {
        "total_customers": total,
        "churn_rate": round(high_risk / total * 100, 2),
        "high_risk_count": int(high_risk),
        "active_rate": round(active / total * 100, 2),
        "avg_credit_limit": round(df['Credit_Limit'].mean(), 2)
    }
