
import pytest
from src.schemas import PivotIn, Scale

# Fixtures like `pivot_client` are now defined in `tests/conftest.py`

def test_unauthorized_access(pivot_client):
    response = pivot_client.post("/analyze_text", json={})
    assert response.status_code == 422  # Missing body

    response = pivot_client.post(
        "/analyze_text",
        headers={"X-API-Key": "wrong-key"},
        json={"text_section": "some text", "lens": ["CHIASMUS"]}
    )
    assert response.status_code == 401

def test_analyze_short_text(pivot_client):
    headers = {"X-API-Key": "test-key"}
    response = pivot_client.post(
        "/analyze_text",
        headers=headers,
        json={"text_section": "short text", "lens": ["CHIASMUS", "GOLDEN"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["points"] == []

def test_analyze_simple_chiastic(pivot_client):
    """Tests detection of a simple, perfect chiastic pattern."""
    headers = {"X-API-Key": "test-key"}
    payload = PivotIn(text_section="a b c b a", scale=Scale.TEXTUAL, lens=["CHIASMUS"])
    response = pivot_client.post("/analyze_text", headers=headers, json=payload.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    points = data[0]["points"]
    assert len(points) == 1
    assert points[0]["detector"] == "chiastic"
    assert points[0]["position"] == 2 # "c" is the center of 5 words (index 2)
    assert points[0]["score"] == 1.0 # Perfect symmetry with window 2

def test_analyze_simple_golden_ratio(pivot_client):
    """Tests detection of a golden ratio point."""
    headers = {"X-API-Key": "test-key"}
    payload = PivotIn(
        text_section="one two three four five six seven eight", lens=["GOLDEN"]
    )
    response = pivot_client.post("/analyze_text", headers=headers, json=payload.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    points = data[0]["points"]
    assert len(points) == 1
    assert points[0]["detector"] == "golden"
    # 8 words / 1.618 ~= 4.94 -> rounded to 5
    assert points[0]["position"] == 5

def test_analyze_valid_text_with_multiple_patterns(pivot_client):
    headers = {"X-API-Key": "test-key"}
    text_with_chiasm = "love hope faith trust faith hope love"  # 7 words
    response = pivot_client.post(
        "/analyze_text",
        headers=headers,
        json={"text_section": text_with_chiasm, "scale": "TEXTUAL", "lens": ["CHIASMUS", "GOLDEN"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

    pivot_out = data[0]
    assert pivot_out["text_section"] == text_with_chiasm
    assert len(pivot_out["points"]) == 2

    points_by_detector = {p["detector"]: p for p in pivot_out["points"]}
    assert "chiastic" in points_by_detector
    assert "golden" in points_by_detector

    # Chiastic check: 7 words, center is index 3. Perfect symmetry.
    chiastic_point = points_by_detector["chiastic"]
    assert chiastic_point["position"] == 3
    assert chiastic_point["score"] == 1.0

    # Golden check: 7 / 1.618 ~= 4.3 -> rounded to 4
    golden_point = points_by_detector["golden"]
    assert golden_point["position"] == 4
    assert golden_point["score"] == 1.0

def test_analyze_text_without_chiastic_pattern(pivot_client):
    headers = {"X-API-Key": "test-key"}
    text = "The LORD is my shepherd I shall not want He maketh me to lie down in green pastures" # 16 words, no repeats
    response = pivot_client.post(
        "/analyze_text",
        headers=headers,
        json={"text_section": text, "scale": "TEXTUAL", "lens": ["CHIASMUS", "GOLDEN"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    pivot_out = data[0]

    # Chiastic detector should find nothing due to no repeated words
    points_by_detector = {p["detector"]: p for p in pivot_out["points"]}
    assert "chiastic" not in points_by_detector
    assert "golden" in points_by_detector

    # Golden Ratio check: 16 / 1.618 ~= 9.88 -> rounded to 10
    golden_point = points_by_detector["golden"]
    assert golden_point["position"] == 10
    assert golden_point["score"] == 1.0
