"""Автотесты для Credit Scoring API (ДЗ 3)."""
from fastapi.testclient import TestClient

from app.main import app


def test_health_check():
    """Health Check: GET /health возвращает {"status": "ok"} и код 200."""
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


def test_predict_happy_path():
    """Happy Path: валидный JSON возвращает 200 и структуру с prediction и score."""
    with TestClient(app) as client:
        payload = {
            "age": 35,
            "income": 60000.0,
            "months_on_book": 24,
            "credit_limit": 50000.0,
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
        assert "score" in data
        assert data["prediction"] in ("low_risk", "high_risk")
        assert isinstance(data["score"], (int, float))
        assert 0 <= data["score"] <= 1


def test_predict_bad_input_missing_fields():
    """Bad Input: неполный JSON возвращает 422 Unprocessable Entity."""
    with TestClient(app) as client:
        payload = {"age": 35, "income": 60000.0}  # нет months_on_book, credit_limit
        response = client.post("/predict", json=payload)
        assert response.status_code == 422


def test_predict_bad_input_wrong_types():
    """Bad Input: неверный тип данных в поле возвращает 422."""
    with TestClient(app) as client:
        payload = {
            "age": "not_a_number",
            "income": 60000.0,
            "months_on_book": 24,
            "credit_limit": 50000.0,
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == 422


def test_predict_bad_input_empty_body():
    """Bad Input: пустое тело запроса возвращает 422."""
    with TestClient(app) as client:
        response = client.post("/predict", json={})
        assert response.status_code == 422
