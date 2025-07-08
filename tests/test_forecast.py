
import pytest
from src.schemas import ForecastRequest

# Fixtures are defined in conftest.py and are used automatically.

def test_forecast_unauthorized(pivot_client):
    req = ForecastRequest(user_id="u1", horizon=5)
    response = pivot_client.post("/forecast", json=req.model_dump())
    assert response.status_code == 422 # Missing X-API-Key header

def test_forecast_success(pivot_client):
    headers = {"X-API-Key": "test-key"}
    req = ForecastRequest(user_id="u1", horizon=5)
    response = pivot_client.post("/forecast", headers=headers, json=req.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert all(isinstance(pt["timestep"], int) for pt in data)
    assert all(0 <= pt["probability"] <= 1 for pt in data)

def test_forecast_for_unknown_user(pivot_client):
    headers = {"X-API-Key": "test-key"}
    req = ForecastRequest(user_id="unknown_user", horizon=5)
    response = pivot_client.post("/forecast", headers=headers, json=req.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    # For a user with no events, probability should still be valid
    assert all(pt["probability"] > 0 for pt in data)
