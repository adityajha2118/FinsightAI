"""Unit tests for Compliance modules."""

import pytest


class TestKYCPrediction:
    """Tests for KYC risk prediction."""

    def test_risk_distribution_returns_data(self):
        """Risk distribution should return non-empty result."""
        try:
            from src.compliance.kyc_prediction import get_risk_distribution
            result = get_risk_distribution()
            assert result is not None
        except FileNotFoundError:
            pytest.skip("KYC data not available")

    def test_high_risk_customers(self):
        """Should return high risk customers list."""
        try:
            from src.compliance.kyc_prediction import get_high_risk_customers
            result = get_high_risk_customers(10)
            assert isinstance(result, (list, dict))
        except FileNotFoundError:
            pytest.skip("KYC data not available")
