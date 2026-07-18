"""Unit tests for Customer Intelligence modules."""

import pytest
from pathlib import Path


class TestSegmentation:
    """Tests for customer segmentation module."""

    def test_segment_distribution_returns_dict(self):
        """Segment distribution should return a dictionary."""
        try:
            from src.customer_intelligence.segmentation import get_segment_distribution
            result = get_segment_distribution()
            assert isinstance(result, dict)
            assert len(result) > 0
        except FileNotFoundError:
            pytest.skip("Processed data not available")

    def test_segment_profiles_returns_list(self):
        """Segment profiles should return a list of dicts."""
        try:
            from src.customer_intelligence.segmentation import get_segment_profiles
            result = get_segment_profiles()
            assert isinstance(result, list)
        except FileNotFoundError:
            pytest.skip("Processed data not available")


class TestChurn:
    """Tests for churn prediction module."""

    def test_churn_distribution_returns_dict(self):
        """Churn distribution should return structured data."""
        try:
            from src.customer_intelligence.churn import get_churn_distribution
            result = get_churn_distribution()
            assert result is not None
        except FileNotFoundError:
            pytest.skip("Processed data not available")

    def test_top_churn_customers(self):
        """Should return top N churn customers."""
        try:
            from src.customer_intelligence.churn import get_top_churn_customers
            result = get_top_churn_customers(5)
            assert isinstance(result, (list, dict))
        except FileNotFoundError:
            pytest.skip("Processed data not available")


class TestConstants:
    """Tests for common constants module."""

    def test_project_root_exists(self):
        """Project root constant should point to valid directory."""
        from src.common.constants import PROJECT_ROOT
        assert PROJECT_ROOT.exists()

    def test_model_paths_defined(self):
        """All model path constants should be defined."""
        from src.common.constants import (
            CHURN_MODELS_DIR, SEGMENTATION_MODELS_DIR,
            CAMPAIGN_MODELS_DIR, KYC_MODELS_DIR
        )
        assert CHURN_MODELS_DIR is not None
        assert SEGMENTATION_MODELS_DIR is not None
