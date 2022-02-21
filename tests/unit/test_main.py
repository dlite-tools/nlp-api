"""Unit test module."""
from fastapi.testclient import TestClient

from src.main import app
from src.version import SERVICE_VERSION

client = TestClient(app)


def test_main_endpoint():
    response = client.get("/")
    data = response.json()

    assert response.status_code == 200
    assert data['version'] == SERVICE_VERSION


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 204


def test_ready_endpoint():
    response = client.get("/ready")

    assert response.status_code == 204
