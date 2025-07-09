
import pytest

# Fixtures like `pivot_client` are now defined in `tests/conftest.py`

def test_unauthorized_access(pivot_client):
    response = pivot_client.post(
        "/analyze_text",
        headers={"X-API-Key": "wrong-key"},
        json={"text": "some text"}
    )
    assert response.status_code == 401

def test_analyze_short_text(pivot_client):
    headers = {"X-API-Key": "test-key"}
    response = pivot_client.post(
        "/analyze_text",
        headers=headers,
        json={"text": "short text"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["chiastic"] is None
    assert data["golden_ratio"] is None

def test_analyze_simple_chiastic(pivot_client):
    """Tests detection of a simple, perfect chiastic pattern."""
    headers = {"X-API-Key": "test-key"}
    payload = {"text": "a b c b a"}
    response = pivot_client.post("/analyze_text", headers=headers, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["chiastic"] is not None
    assert data["chiastic"]["type"] == "Chiastic"
    assert data["chiastic"]["center"] == "c"
    assert data["chiastic"]["score"] == 1.0
    
def test_analyze_simple_golden_ratio(pivot_client):
    """Tests detection of a golden ratio point."""
    headers = {"X-API-Key": "test-key"}
    payload = {"text": "one two three four five six seven eight"}
    response = pivot_client.post("/analyze_text", headers=headers, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["golden_ratio"] is not None
    assert data["golden_ratio"]["type"] == "Golden Ratio"
    assert data["golden_ratio"]["total_words"] == 8
    # 8 words / 1.618 ~= 4.94 -> rounded to 5
    assert data["golden_ratio"]["major_pivot"]["index"] == 5

def test_analyze_valid_text_with_multiple_patterns(pivot_client):
    headers = {"X-API-Key": "test-key"}
    text = "love hope faith trust faith hope love"  # 7 words
    response = pivot_client.post(
        "/analyze_text",
        headers=headers,
        json={"text": text},
    )
    assert response.status_code == 200
    data = response.json()
    
    # Chiastic check
    assert data["chiastic"] is not None
    assert data["chiastic"]["center"] == "trust"
    assert data["chiastic"]["score"] == 1.0

    # Golden check: 7 / 1.618 ~= 4.3 -> rounded to 4
    assert data["golden_ratio"] is not None
    assert data["golden_ratio"]["major_pivot"]["index"] == 4

def test_analyze_text_without_chiastic_pattern(pivot_client):
    headers = {"X-API-Key": "test-key"}
    text = "The LORD is my shepherd I shall not want He maketh me to lie down in green pastures" # 16 words, no repeats
    response = pivot_client.post(
        "/analyze_text",
        headers=headers,
        json={"text": text},
    )
    assert response.status_code == 200
    data = response.json()
    
    assert data["chiastic"] is None
    
    # Golden Ratio check: 16 / 1.618 ~= 9.88 -> rounded to 10
    assert data["golden_ratio"] is not None
    assert data["golden_ratio"]["major_pivot"]["index"] == 10
