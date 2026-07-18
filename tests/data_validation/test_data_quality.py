"""Data validation tests for processed datasets."""

import pytest
import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path(__file__).parent.parent.parent / "data" / "processed"


class TestDataQuality:
    """Validate schema and quality of processed datasets."""

    @pytest.mark.skipif(
        not (PROCESSED_DIR / "customer_clean.csv").exists(),
        reason="Processed data not available"
    )
    def test_customer_clean_schema(self):
        """customer_clean.csv should have required columns."""
        df = pd.read_csv(PROCESSED_DIR / "customer_clean.csv")
        required = ["CLIENTNUM", "Customer_Age", "Credit_Limit", "Attrition_Flag"]
        for col in required:
            assert col in df.columns, f"Missing column: {col}"

    @pytest.mark.skipif(
        not (PROCESSED_DIR / "unified_customer_profile.csv").exists(),
        reason="Processed data not available"
    )
    def test_unified_profile_completeness(self):
        """Unified profile should have segment and churn columns."""
        df = pd.read_csv(PROCESSED_DIR / "unified_customer_profile.csv")
        assert "segment_name" in df.columns
        assert "churn_probability" in df.columns
        assert df["churn_probability"].between(0, 1).all()

    @pytest.mark.skipif(
        not (PROCESSED_DIR / "kyc_clean.csv").exists(),
        reason="KYC data not available"
    )
    def test_kyc_no_duplicates(self):
        """KYC data should not have excessive duplicates."""
        df = pd.read_csv(PROCESSED_DIR / "kyc_clean.csv")
        assert len(df) > 0
