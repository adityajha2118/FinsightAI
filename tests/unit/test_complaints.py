"""Unit tests for Complaint Intelligence modules."""

import pytest


class TestValidators:
    """Tests for input validation."""

    def test_valid_narrative(self):
        """Valid narrative should pass validation."""
        from src.utils.validators import validate_narrative
        result = validate_narrative("This is a valid complaint narrative that is long enough.")
        assert len(result) >= 20

    def test_short_narrative_raises(self):
        """Short narrative should raise ValueError."""
        from src.utils.validators import validate_narrative
        with pytest.raises(ValueError):
            validate_narrative("Too short")

    def test_empty_narrative_raises(self):
        """Empty narrative should raise ValueError."""
        from src.utils.validators import validate_narrative
        with pytest.raises(ValueError):
            validate_narrative("")


class TestResponseEvaluator:
    """Tests for LLM response quality evaluation."""

    def test_good_response_scores_high(self):
        """Professional, empathetic response should score well."""
        from src.genai.evaluators.response_evaluator import evaluate_response
        response = "We understand your frustration and sincerely apologize. Our team will investigate this matter and assist you promptly."
        result = evaluate_response(response, {"category": "Billing", "emotion": "Anger", "priority_level": "HIGH"})
        assert result["quality_score"] >= 0.5
        assert result["is_professional"] is True
        assert result["is_empathetic"] is True
