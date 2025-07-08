
import pytest
from datetime import datetime, timedelta
import sqlite_utils
import json
from src.cme_service import DB_PATH
from src import db as review_db
import uuid

# All fixtures are now defined in `tests/conftest.py` and are automatically used.

def test_unauthorized_access(cme_client):
    response = cme_client.post("/add_verse", json={})
    assert response.status_code == 422  # No header

    response = cme_client.post("/add_verse", headers={"X-API-Key": "wrong-key"}, json={
        "verse_id": "Test_1_1", "text": "Test text"
    })
    assert response.status_code == 401

def test_add_verse(cme_client):
    headers = {"X-API-Key": "test-key"}
    verse_data = {
        "verse_id": "John_3_16",
        "text": "For God so loved the world...",
        "covenant_tags": ["Love", "Atonement"],
        "emotion_codes": ["Love"],
        "notes": "A test note."
    }
    response = cme_client.post("/add_verse", headers=headers, json=verse_data)
    assert response.status_code == 201
    assert response.json() == {"verse_id": "John_3_16", "status": "created_or_updated"}

    # Check if it's in the DB
    db = sqlite_utils.Database(DB_PATH)
    row = db["verses"].get("John_3_16")
    assert row["text"] == "For God so loved the world..."
    assert row["notes"] == "A test note."
    assert row["pivot"] is None

def test_add_verse_with_pivot_data(cme_client):
    headers = {"X-API-Key": "test-key"}
    pivot_data = {
        "type": "Chiastic",
        "center": "C",
        "elements": ["A <-> A", "B <-> B"],
        "score": 1.0,
        "match_count": 2,
        "depth": 2
    }
    verse_data = {
        "verse_id": "Test_Pivot_1",
        "text": "Test with pivot",
        "pivot": pivot_data
    }
    response = cme_client.post("/add_verse", headers=headers, json=verse_data)
    assert response.status_code == 201

    db = sqlite_utils.Database(DB_PATH)
    row = db["verses"].get("Test_Pivot_1")
    assert row["pivot"] is not None
    retrieved_pivot = json.loads(row["pivot"])
    assert retrieved_pivot["type"] == "Chiastic"
    assert retrieved_pivot["score"] == 1.0

def test_get_flashcards_empty(cme_client):
    headers = {"X-API-Key": "test-key"}
    response = cme_client.get("/flashcards", headers=headers)
    assert response.status_code == 200
    assert response.json() == []

def test_get_due_flashcard(cme_client):
    headers = {"X-API-Key": "test-key"}
    verse_data = {
        "verse_id": "Gen_1_1",
        "text": "In the beginning...",
        "next_due": (datetime.utcnow() - timedelta(days=1)).isoformat()  # Due yesterday
    }
    cme_client.post("/add_verse", headers=headers, json=verse_data)

    response = cme_client.get("/flashcards", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["verse_id"] == "Gen_1_1"

def test_review_verse(cme_client):
    headers = {"X-API-Key": "test-key"}
    verse_data = {"verse_id": "Phil_4_13", "text": "I can do all things..."}
    cme_client.post("/add_verse", headers=headers, json=verse_data)

    # Review with "Good" quality (a passing score in the new algorithm is >= 3)
    review_data = {"quality": 3}
    response = cme_client.post("/review_verse/Phil_4_13", headers=headers, json=review_data)
    assert response.status_code == 200
    assert response.json()["status"] == "review_recorded"

    db = sqlite_utils.Database(DB_PATH)
    row = db["verses"].get("Phil_4_13")
    assert row["repetitions"] == 1
    assert row["interval"] == 1  # First interval is 1 day
    # Check if next_due is roughly 1 day from now
    next_due_dt = datetime.fromisoformat(row["next_due"].replace("Z", "+00:00"))
    assert (next_due_dt - datetime.utcnow()).days >= 0

def test_review_nonexistent_verse(cme_client):
    headers = {"X-API-Key": "test-key"}
    response = cme_client.post("/review_verse/Non_Existent_1_1", headers=headers, json={"quality": 3})
    assert response.status_code == 404

def test_user_review(cme_client):
    headers = {"X-API-Key": "test-key"}
    verse_id = "1Cor_13_4"
    user_id = str(uuid.uuid4())
    
    # Add the verse first (though it's not strictly required by the review logic)
    cme_client.post("/add_verse", headers=headers, json={"verse_id": verse_id, "text": "Love is patient..."})
    
    # First review (q=5, perfect)
    review_data = {"user_id": user_id, "verse_id": verse_id, "q": 5}
    response = cme_client.post("/review", headers=headers, json=review_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["verse_id"] == verse_id
    assert "Your next review is in 1 days" in data["message"]

    # Verify state in DB
    db = review_db.get_db_conn()
    state = db["reviews"].get((user_id, verse_id))
    assert state is not None
    assert state["repetition_count"] == 1
    assert state["interval"] == 1
    assert state["ease_factor"] > 2.5 # Easiness should increase
    
    # Second review (q=4, good)
    review_data_2 = {"user_id": user_id, "verse_id": verse_id, "q": 4}
    response_2 = cme_client.post("/review", headers=headers, json=review_data_2)
    assert response_2.status_code == 200
    data_2 = response_2.json()
    assert "Your next review is in 6 days" in data_2["message"]

    # Verify state in DB again
    state_2 = db["reviews"].get((user_id, verse_id))
    assert state_2["repetition_count"] == 2
    assert state_2["interval"] == 6

def test_user_review_failure(cme_client):
    headers = {"X-API-Key": "test-key"}
    verse_id = "Prov_3_5"
    user_id = str(uuid.uuid4())
    
    # Review with a failing score (q=1)
    review_data = {"user_id": user_id, "verse_id": verse_id, "q": 1}
    response = cme_client.post("/review", headers=headers, json=review_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "Your next review is in 1 days" in data["message"]
    
    # Verify state in DB
    db = review_db.get_db_conn()
    state = db["reviews"].get((user_id, verse_id))
    assert state["repetition_count"] == 0 # Reps reset
    assert state["interval"] == 1 # Interval resets
    assert state["ease_factor"] < 2.5 # Easiness should decrease
