"""FinSight AI — Global Constants and Path Definitions."""

from pathlib import Path

# ── Project Root ─────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# ── Data Paths ───────────────────────────────────────────────
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
FEATURE_STORE_DIR = DATA_DIR / "feature_store"
SAMPLE_DATA_DIR = DATA_DIR / "sample_data"

# ── Model Paths ──────────────────────────────────────────────
MODELS_DIR = PROJECT_ROOT / "models"
CHURN_MODELS_DIR = MODELS_DIR / "churn"
SEGMENTATION_MODELS_DIR = MODELS_DIR / "segmentation"
INACTIVITY_MODELS_DIR = MODELS_DIR / "inactivity"
CAMPAIGN_MODELS_DIR = MODELS_DIR / "campaign"
KYC_MODELS_DIR = MODELS_DIR / "kyc"
ESCALATION_MODELS_DIR = MODELS_DIR / "escalation"

# ── Config Paths ─────────────────────────────────────────────
CONFIGS_DIR = PROJECT_ROOT / "configs"
PROMPTS_DIR = PROJECT_ROOT / "prompts"

# ── Application Constants ────────────────────────────────────
APP_NAME = "FinSight AI"
APP_VERSION = "1.0.0"
DEFAULT_LLM_PROVIDER = "gemini"
DEFAULT_LLM_TEMPERATURE = 0.3

# ── Risk Tier Thresholds ─────────────────────────────────────
RISK_CRITICAL_THRESHOLD = 0.75
RISK_HIGH_THRESHOLD = 0.50
RISK_MEDIUM_THRESHOLD = 0.25

# ── Churn Thresholds ─────────────────────────────────────────
CHURN_HIGH_THRESHOLD = 0.70
INACTIVITY_FLAG_THRESHOLD = 0.30
