
import os
import pytest
from fastapi.testclient import TestClient

# Set a dummy API key for testing
os.environ["SANCTUM_API_KEY"] = "test-key"
from src.pivot_service import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_unauthorized_access(client):
    response = client.post("/analyze_text", json={})
    assert response.status_code == 422 # Missing body

    response = client.post("/analyze_text", headers={"X-API-Key": "wrong-key"}, json={"text": "some text"})
    assert response.status_code == 401

def test_analyze_short_text(client):
    headers = {"X-API-Key": "test-key"}
    response = client.post("/analyze_text", headers=headers, json={"text": "short text"})
    # It should return empty analysis as text is too short
    assert response.status_code == 200
    data = response.json()
    assert data["chiastic"] is None
    assert data["golden_ratio"] is None

def test_analyze_valid_text(client):
    headers = {"X-API-Key": "test-key"}
    text = "The LORD is my shepherd I shall not want He maketh me to lie down in green pastures"
    # 16 words
    response = client.post("/analyze_text", headers=headers, json={"text": text})
    assert response.status_code == 200
    data = response.json()

    # Chiastic check
    assert data["chiastic"]["type"] == "Chiastic"
    assert data["chiastic"]["center"] == "i" # 8th word out of 16 (0-indexed)
    assert len(data["chiastic"]["elements"]) == 8
    assert data["chiastic"]["elements"][0] == "the <-> pastures"

    # Golden Ratio check
    # 16 / 1.618 ~= 9.88 -> rounded to 10
    assert data["golden_ratio"]["type"] == "Golden Ratio"
    assert data["golden_ratio"]["total_words"] == 16
    assert data["golden_ratio"]["pivot_word_index"] == 10
    assert data["golden_ratio"]["pivot_word"] == "lie" # 10th word
