from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_evaluation_requires_auth() -> None:
    response = client.post(
        "/v1/evaluations",
        json={"service": "llm-api", "availability": 99.9, "p95_latency_ms": 1000, "error_rate": 0.001},
    )
    assert response.status_code == 401


def test_evaluation_api() -> None:
    key = get_settings().api_key
    response = client.post(
        "/v1/evaluations",
        headers={"X-API-Key": key},
        json={"service": "llm-api", "availability": 99.99, "p95_latency_ms": 1000, "error_rate": 0.001},
    )
    assert response.status_code == 200
    assert response.json()["severity"] == "healthy"
