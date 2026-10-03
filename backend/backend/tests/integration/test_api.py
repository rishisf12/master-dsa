import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.session import get_session
from tests.conftest import get_test_session


client = TestClient(app)


class TestAPI:
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert "Master DSA API" in response.json()["message"]

    def test_verify_admin_success(self):
        """Test admin verification with correct username."""
        app.dependency_overrides[get_session] = get_test_session
        
        response = client.post(
            "/api/v1/auth/verify",
            json={"username": "admin"}
        )
        assert response.status_code == 200
        assert response.json()["valid"] is True

    def test_verify_admin_failure(self):
        """Test admin verification with incorrect username."""
        response = client.post(
            "/api/v1/auth/verify",
            json={"username": "wrong"}
        )
        assert response.status_code == 200
        assert response.json()["valid"] is False