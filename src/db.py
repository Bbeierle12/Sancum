import os
import sqlite_utils
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'sanctum.db')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_db_conn():
    """Returns a database connection and ensures tables exist."""
    db = sqlite_utils.Database(DB_PATH)
    if "reviews" not in db.table_names():
        db["reviews"].create({
            "user_id": str,
            "verse_id": str,
            "ease_factor": float,
            "repetition_count": int,
            "interval": int,
            "next_due": datetime,
        }, pk=("user_id", "verse_id"))
        print("Database table 'reviews' created.")
    return db

def get_review_state(user_id: str, verse_id: str) -> dict | None:
    """Fetches the SM-2 review state for a user and verse."""
    db = get_db_conn()
    try:
        return db["reviews"].get((user_id, verse_id))
    except sqlite_utils.db.NotFoundError:
        return None

def save_review_state(user_id: str, verse_id: str, new_state: dict):
    """Saves or updates the SM-2 review state for a user and verse."""
    db = get_db_conn()
    record = {
        "user_id": user_id,
        "verse_id": verse_id,
        **new_state
    }
    db["reviews"].upsert(record, pk=("user_id", "verse_id"))
