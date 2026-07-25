"""FinSight AI — Prediction API Router.

Exposes ML model prediction endpoints for churn, campaign, and compliance.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from src.ml import inference

router = APIRouter(prefix="/api/predict", tags=["ML Predictions"])


# ── Request Schemas ───────────────────────────────────────────

class ChurnRequest(BaseModel):
    """Customer features for churn prediction."""
    customer_age: int = Field(45, description="Customer age")
    dependent_count: int = 3
    months_on_book: int = 39
    months_inactive_12_mon: int = 1
    contacts_count_12_mon: int = 3
    credit_limit: float = 12691
    total_revolving_bal: float = 777
    avg_open_to_buy: float = 11914
    total_amt_chng_q4_q1: float = 1.335
    total_trans_amt: float = 1144
    total_trans_ct: int = 42
    total_ct_chng_q4_q1: float = 1.625
    avg_utilization_ratio: float = 0.061
    income_category: str = "$60K - $80K"
    card_category: str = "Blue"
    gender: str = "M"
    education_level: str = "High School"
    marital_status: str = "Married"


class CampaignRequest(BaseModel):
    """Customer features for campaign conversion prediction."""
    age: int = 40
    job: str = "admin."
    marital: str = "married"
    education: str = "university.degree"
    default_credit: str = "no"
    housing: str = "yes"
    loan: str = "no"
    contact: str = "cellular"
    month: str = "may"
    day_of_week: str = "mon"
    duration: int = 200
    campaign_count: int = 1
    pdays: int = 999
    previous: int = 0
    poutcome: str = "nonexistent"
    emp_var_rate: float = 1.1
    cons_price_idx: float = 93.994
    cons_conf_idx: float = -36.4
    euribor3m: float = 4.857
    nr_employed: float = 5191.0


class ComplianceRequest(BaseModel):
    """Entity features for KYC compliance risk prediction."""
    pep_flag: int = Field(0, ge=0, le=1)
    sanctions_flag: int = Field(0, ge=0, le=1)
    ofac_country_flag: int = Field(0, ge=0, le=1)
    structuring_pattern_flag: int = Field(0, ge=0, le=1)
    rapid_movement_flag: int = Field(0, ge=0, le=1)
    trade_mispricing_flag: int = Field(0, ge=0, le=1)
    ownership_opacity_score: float = Field(0.0, ge=0.0, le=1.0)
    sector_risk: str = "Low"
    transaction_count: int = 0


# ── Endpoints ─────────────────────────────────────────────────

@router.post("/churn")
async def predict_churn(request: ChurnRequest):
    """Predict customer churn probability."""
    try:
        return inference.predict_churn(request.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/campaign")
async def predict_campaign(request: CampaignRequest):
    """Predict campaign conversion probability."""
    try:
        return inference.predict_campaign(request.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compliance")
async def predict_compliance(request: ComplianceRequest):
    """Predict KYC compliance risk tier."""
    try:
        return inference.predict_compliance(request.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
