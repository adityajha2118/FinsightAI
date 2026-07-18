"""API endpoint tests using FastAPI TestClient."""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create FastAPI test client."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from main import app
    return TestClient(app)


class TestHealthCheck:
    """Tests for health check endpoint."""

    def test_health_returns_ok(self, client):
        """Health endpoint should return status ok."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data


class TestCustomerEndpoints:
    """Tests for customer API endpoints."""

    @pytest.mark.api
    def test_segments_endpoint(self, client):
        """Segments endpoint should return data."""
        response = client.get("/api/customers/segments")
        assert response.status_code == 200

    @pytest.mark.api
    def test_invalid_profile_returns_404(self, client):
        """Invalid client ID should return 404."""
        response = client.get("/api/customers/profile/INVALID_ID_999999")
        assert response.status_code == 404


class TestComplaintEndpoints:
    """Tests for complaint API endpoints."""

    @pytest.mark.api
    def test_short_narrative_returns_400(self, client):
        """Short narrative should return 400."""
        response = client.post("/api/complaints/process", json={"narrative": "short"})
        assert response.status_code == 400
