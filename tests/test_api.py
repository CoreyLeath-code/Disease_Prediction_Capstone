"""Contract and failure-mode tests for the educational screening API."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

VALID_PAYLOAD = {
    "age": 52,
    "bmi": 28.4,
    "systolic_bp": 134.0,
    "diastolic_bp": 84.0,
    "glucose": 112.0,
    "insulin": 118.0,
    "skin_thickness": 30.0,
    "cholesterol": 216.0,
    "hba1c": 5.9,
}


def test_root_contract_discloses_non_clinical_use() -> None:
    response = client.get("/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "Disease_Prediction_Capstone"
    assert payload["clinical_use"] is False
    assert "not a diagnosis" in payload["disclaimer"].lower()


def test_health_contract() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "disease-prediction-capstone-api",
        "version": "2.0.0",
        "clinical_use": False,
    }


def test_predict_returns_explainable_moderate_result() -> None:
    response = client.post("/predict", json=VALID_PAYLOAD)

    assert response.status_code == 200
    payload = response.json()
    assert payload["category"] == "moderate"
    assert 0.0 <= payload["score"] <= 100.0
    assert payload["contributors"]
    assert payload["backend"] == "deterministic-educational-screening-baseline"
    assert payload["api_version"] == "2.0.0"


def test_predict_is_deterministic() -> None:
    first = client.post("/predict", json=VALID_PAYLOAD)
    second = client.post("/predict", json=VALID_PAYLOAD)

    assert first.status_code == second.status_code == 200
    assert first.json() == second.json()


def test_predict_rejects_invalid_blood_pressure_order() -> None:
    payload = {**VALID_PAYLOAD, "systolic_bp": 80.0, "diastolic_bp": 90.0}

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_predict_rejects_out_of_range_input() -> None:
    payload = {**VALID_PAYLOAD, "glucose": -1.0}

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_predict_rejects_unknown_fields() -> None:
    payload = {**VALID_PAYLOAD, "patient_name": "do-not-collect"}

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_examples_are_fictional_and_assessable() -> None:
    response = client.get("/examples")

    assert response.status_code == 200
    payload = response.json()
    assert set(payload) == {
        "Lower indicator example",
        "Moderate indicator example",
        "Elevated indicator example",
    }
    assert payload["Elevated indicator example"]["assessment"]["category"] == "elevated"


def test_metrics_endpoint_exposes_application_counters() -> None:
    response = client.get("/metrics")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert "disease_capstone_screening_requests_total" in response.text
