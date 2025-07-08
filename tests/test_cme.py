
import os
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import sqlite_utils
import json

# Set a dummy API key for testing
os.environ["SANCTUM_API_KEY"] = "test-key"
from src.cme_service import app, DB_PATH

@pytest.fixture(scope="module")
def client():
    # Use an in-memory database for tests
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    with TestClient(app) as c:
        yield c
    
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

@pytest.fixture(autouse=True)
def clear_db_before_each_test():
    # This ensures the DB is fresh for every test function
    if os.path.exists(DB_PATH):
        db = sqlite_utils.Database(DB_PATH)
        if "verses" in db.table_names():
            db["verses"].delete_where()
            # Re-run startup to ensure table is created again
            with TestClient(app):
                pass

def test_unauthorized_access(client):
    response = client.post("/add_verse", json={})
    assert response.status_code == 422 # No header
    
    response = client.post("/add_verse", headers={"X-API-Key": "wrong-key"}, json={
        "verse_id": "Test_1_1", "text": "Test text"
    })
    assert response.status_code == 401

def test_add_verse(client):
    headers = {"X-API-Key": "test-key"}
    verse_data = {
        "verse_id": "John_3_16",
        "text": "For God so loved the world...",
        "covenant_tags": ["Love", "Atonement"],
        "emotion_codes": ["Love"],
        "notes": "A test note."
    }
    response = client.post("/add_verse", headers=headers, json=verse_data)
    assert response.status_code == 201
    assert response.json() == {"verse_id": "John_3_16", "status": "created_or_updated"}
    
    # Check if it's in the DB
    db = sqlite_utils.Database(DB_PATH)
    row = db["verses"].get("John_3_16")
    assert row["text"] == "For God so loved the world..."
    assert row["notes"] == "A test note."
    assert row["pivot"] is None

def test_add_verse_with_pivot_data(client):
    headers = {"X-API-Key": "test-key"}
    pivot_data = {
        "type": "Chiastic",
        "center": "C",
        "elements": ["A <-> A", "B <-> B"],
        "score": 1.0
    }
    verse_data = {
        "verse_id": "Test_Pivot_1",
        "text": "Test with pivot",
        "pivot": pivot_data
    }
    response = client.post("/add_verse", headers=headers, json=verse_data)
    assert response.status_code == 201

    db = sqlite_utils.Database(DB_PATH)
    row = db["verses"].get("Test_Pivot_1")
    assert row["pivot"] is not None
    retrieved_pivot = json.loads(row["pivot"])
    assert retrieved_pivot["type"] == "Chiastic"
    assert retrieved_pivot["score"] == 1.0

def test_get_flashcards_empty(client):
    headers = {"X-API-Key": "test-key"}
    response = client.get("/flashcards", headers=headers)
    assert response.status_code == 200
    assert response.json() == []

def test_get_due_flashcard(client):
    headers = {"X-API-Key": "test-key"}
    verse_data = {
        "verse_id": "Gen_1_1",
        "text": "In the beginning...",
        "next_due": (datetime.utcnow() - timedelta(days=1)).isoformat() # Due yesterday
    }
    client.post("/add_verse", headers=headers, json=verse_data)
    
    response = client.get("/flashcards", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["verse_id"] == "Gen_1_1"

def test_review_verse(client):
    headers = {"X-API-Key": "test-key"}
    verse_data = {"verse_id": "Phil_4_13", "text": "I can do all things..."}
    client.post("/add_verse", headers=headers, json=verse_data)

    # Review with "Good" quality
    review_data = {"quality": 2}
    response = client.post("/review_verse/Phil_4_13", headers=headers, json=review_data)
    assert response.status_code == 200
    assert response.json()["status"] == "review_recorded"

    db = sqlite_utils.Database(DB_PATH)
    row = db["verses"].get("Phil_4_13")
    assert row["repetitions"] == 1
    assert row["interval"] == 1 # First interval is 1 day
    # Check if next_due is roughly 1 day from now
    next_due_dt = datetime.fromisoformat(row["next_due"].replace("Z", "+00:00"))
    assert (next_due_dt - datetime.utcnow()).days >= 0

def test_review_nonexistent_verse(client):
    headers = {"X-API-Key": "test-key"}
    response = client.post("/review_verse/Non_Existent_1_1", headers=headers, json={"quality": 3})
    assert response.status_code == 404
