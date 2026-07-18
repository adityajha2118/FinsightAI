from src.agents.complaint_agent import run_complaint_agent
from src.customer_intelligence.profile_builder import get_unified_profile
from src.compliance.kyc_prediction import predict_kyc_risk

def process_complaint(narrative: str) -> dict:
    """Route complaint narrative through AI agent pipeline."""
    return run_complaint_agent(narrative)

def get_customer_profile(client_id: str) -> dict:
    """Retrieve unified customer profile for a CLIENTNUM."""
    return get_unified_profile(client_id)

def get_kyc_action(features: dict) -> dict:
    """Assess KYC risk for provided feature dict."""
    return predict_kyc_risk(features)
