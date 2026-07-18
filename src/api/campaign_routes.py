"""FinSight AI — Campaign Analytics API Routes."""

from fastapi import APIRouter
from pydantic import BaseModel

from src.campaign_analytics import campaign_analysis, campaign_prediction

router = APIRouter(prefix="/api/campaign", tags=["Campaign Analytics"])


class CampaignFeaturesRequest(BaseModel):
    """Input features for campaign conversion prediction."""
    age: float = 0.0
    job: int = 0
    marital: int = 0
    education: int = 0
    default: int = 0
    housing: int = 0
    loan: int = 0
    contact: int = 0
    month: int = 0
    campaign: float = 0.0
    pdays: float = 0.0
    previous: float = 0.0
    poutcome: int = 0
    emp_var_rate: float = 0.0
    cons_price_idx: float = 0.0
    cons_conf_idx: float = 0.0
    euribor3m: float = 0.0
    nr_employed: float = 0.0
    contacted_before: int = 0
    campaign_intensity: float = 0.0


@router.get("/stats")
async def get_campaign_stats():
    """Full campaign statistics including success rates and channel breakdowns."""
    return campaign_analysis.get_full_campaign_stats()


@router.post("/predict")
async def predict_campaign(request: CampaignFeaturesRequest):
    """Predict campaign conversion probability for given features."""
    return campaign_prediction.predict_campaign_success(request.dict())
