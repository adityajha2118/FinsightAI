"""FinSight AI — Compliance & KYC API Routes."""

from fastapi import APIRouter
from pydantic import BaseModel

from src.compliance import kyc_prediction

router = APIRouter(prefix="/api/compliance", tags=["Compliance"])


class KYCFeaturesRequest(BaseModel):
    """Input features for KYC risk prediction."""
    ofac_match_flag: int = 0
    fatf_txn_flag: int = 0
    structuring_pattern_flag: int = 0
    rapid_movement_flag: int = 0
    trade_mispricing_flag: int = 0
    pep_flag: int = 0
    sanctions_flag: int = 0
    fatf_entity_flag: int = 0
    ofac_country_flag: int = 0
    sectoral_sanctions_flag: int = 0
    ownership_opacity_score: float = 0.0
    sector_risk: str = "Low"


@router.get("/risk/distribution")
async def get_risk_distribution():
    """KYC risk tier distribution counts."""
    return kyc_prediction.get_risk_distribution()


@router.get("/risk/high")
async def get_high_risk(n: int = 50):
    """Top N high-risk entities."""
    return kyc_prediction.get_high_risk_customers(n)


@router.post("/risk/predict")
async def predict_kyc(request: KYCFeaturesRequest):
    """Predict KYC risk tier for given features."""
    return kyc_prediction.predict_kyc_risk(request.dict())
