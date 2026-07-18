from pathlib import Path
import pandas as pd
from dotenv import load_dotenv; load_dotenv()

INACTIVITY_PATH = Path("data/processed/inactivity_scores.csv")
BANK_TX_PATH    = Path("data/processed/bank_tx_activity.csv")

def get_activity_distribution() -> dict:
    """Return {activity_category: count} from inactivity_scores.csv."""
    df = pd.read_csv(INACTIVITY_PATH)
    return df['activity_category'].value_counts().to_dict()

def get_future_churn_watchlist(n: int = 100) -> list:
    """Return top n future churn candidates sorted by activity_score ascending."""
    df = pd.read_csv(INACTIVITY_PATH)
    return df[df['future_churn_candidate'] == True].sort_values('activity_score', ascending=True).head(n).to_dict(orient='records')

def get_bank_tx_summary() -> dict:
    """Return summary stats from bank_tx_activity.csv."""
    df = pd.read_csv(BANK_TX_PATH)
    return {
        "total_accounts": len(df),
        "high_risk_accounts": int(df['high_risk_account'].sum()),
        "avg_days_since_last": float(df['days_since_last'].mean()),
        "avg_balance": float(df['avg_balance'].mean())
    }
