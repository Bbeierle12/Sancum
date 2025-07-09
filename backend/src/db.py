"""SQLite helper functions for spaced-repetition data."""

import os
from datetime import datetime
from typing import Optional, Dict

import sqlite_utils
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "sanctum.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def _ensure_tables(db: sqlite_utils.Database) -> None:
    if "verse_reviews" not in db.table_names():
        db["verse_reviews"].create(
            {
                "user_id": str,
                "verse_id": str,
                "ease_factor": float,
                "repetition_count": int,
                "interval": int,
                "next_due": datetime,
            },
            pk=("user_id", "verse_id"),
        )
        print("Database table 'verse_reviews' created.")


def connect() -> sqlite_utils.Database:
    """Return a database connection ensuring tables exist."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    db = sqlite_utils.Database(conn)
    _ensure_tables(db)
    return db


def get_review_state(user_id: str, verse_id: str) -> Optional[Dict]:
    """Fetches the SM-2 review state for a user and verse."""
    db = connect()
    try:
        return db["verse_reviews"].get((user_id, verse_id))
    except sqlite_utils.db.NotFoundError:
        return None
    finally:
        db.close()


def save_review_state(user_id: str, verse_id: str, state: Dict) -> None:
    """Saves or updates the SM-2 review state for a user and verse."""
    db = connect()
    try:
        record = dict(state)
        record.update({"user_id": user_id, "verse_id": verse_id})
        db["verse_reviews"].upsert(record, pk=("user_id", "verse_id"))
    finally:
        db.close()
