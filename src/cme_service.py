
import os
import sqlite_utils
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta

# --- Configuration ---
API_KEY = os.getenv("SANCTUM_API_KEY")
if not API_KEY:
    raise ValueError("SANCTUM_API_KEY environment variable not set.")

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'sanctum.db')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
db = sqlite_utils.Database(DB_PATH)

app = FastAPI(
    title="Sanctum Covenant Memory Engine (CME)",
    description="A service to manage scripture flashcards with spaced repetition.",
    version="1.0.0",
)

# --- Pydantic Models ---
class Verse(BaseModel):
    verse_id: str = Field(..., description="Canonical verse reference, e.g., 'John_3_16'")
    text: str = Field(..., description="The full text of the scripture.")
    covenant_tags: Optional[List[str]] = []
    emotion_codes: Optional[List[str]] = []
    notes: Optional[str] = ""
    # SM-2 Spaced Repetition Fields
    repetitions: int = 0
    easiness_factor: float = 2.5
    interval: int = 0 # in days
    next_due: datetime = Field(default_factory=datetime.utcnow)

class VerseUpdate(BaseModel):
    quality: int = Field(..., ge=0, le=4, description="Recall quality: 0-Again, 1-Hard, 2-Good, 3-Easy, 4-Perfect")

# --- Database Setup ---
def init_db():
    if "verses" not in db.table_names():
        db["verses"].create({
            "verse_id": str,
            "text": str,
            "covenant_tags": str, # Stored as JSON string
            "emotion_codes": str, # Stored as JSON string
            "notes": str,
            "repetitions": int,
            "easiness_factor": float,
            "interval": int,
            "next_due": datetime,
        }, pk="verse_id")
        print("Database table 'verses' created.")

# --- API Key Dependency ---
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# --- Spaced Repetition Logic (Simplified SM-2) ---
def update_sm2(verse: dict, quality: int):
    """
    Updates SM-2 parameters based on recall quality.
    A simplified approach for demonstration.
    """
    if quality < 2: # If "Again" or "Hard"
        verse["repetitions"] = 0
        verse["interval"] = 1
    else:
        verse["repetitions"] += 1
        if verse["repetitions"] == 1:
            verse["interval"] = 1
        elif verse["repetitions"] == 2:
            verse["interval"] = 6
        else:
            verse["interval"] = round(verse["interval"] * verse["easiness_factor"])

        # Adjust easiness factor
        verse["easiness_factor"] += (0.1 - (4 - quality) * (0.08 + (4 - quality) * 0.02))
        if verse["easiness_factor"] < 1.3:
            verse["easiness_factor"] = 1.3
    
    verse["next_due"] = datetime.utcnow() + timedelta(days=verse["interval"])
    return verse


# --- API Endpoints ---
@app.on_event("startup")
async def startup_event():
    init_db()

@app.post("/add_verse", status_code=201, dependencies=[Depends(verify_api_key)])
async def add_verse(verse: Verse):
    """Adds a new verse to the memory database."""
    try:
        import json
        verse_dict = verse.model_dump()
        verse_dict["covenant_tags"] = json.dumps(verse.covenant_tags)
        verse_dict["emotion_codes"] = json.dumps(verse.emotion_codes)
        
        db["verses"].upsert(verse_dict, pk="verse_id")
        return {"verse_id": verse.verse_id, "status": "created_or_updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/flashcards", response_model=List[Verse], dependencies=[Depends(verify_api_key)])
async def get_flashcards(limit: int = 10):
    """Retrieves all verses due for review today."""
    import json
    now = datetime.utcnow()
    # Using 'lt' because we want anything past due
    due_verses = db["verses"].rows_where("next_due < ?", [now.isoformat()], order_by="next_due", limit=limit)
    
    results = []
    for verse in due_verses:
        verse['covenant_tags'] = json.loads(verse['covenant_tags'])
        verse['emotion_codes'] = json.loads(verse['emotion_codes'])
        results.append(Verse(**verse))
        
    return results

@app.post("/review_verse/{verse_id}", status_code=200, dependencies=[Depends(verify_api_key)])
async def review_verse(verse_id: str, update: VerseUpdate):
    """Updates a verse's spaced repetition data after a review."""
    import json
    try:
        verse_row = db["verses"].get(verse_id)
    except sqlite_utils.db.NotFoundError:
        raise HTTPException(status_code=404, detail="Verse not found")

    updated_verse_data = update_sm2(verse_row, update.quality)

    # Convert lists back to JSON strings for storage
    updated_verse_data["covenant_tags"] = json.dumps(updated_verse_data["covenant_tags"])
    updated_verse_data["emotion_codes"] = json.dumps(updated_verse_data["emotion_codes"])

    db["verses"].update(verse_id, updated_verse_data)
    return {"verse_id": verse_id, "status": "review_recorded", "next_due": updated_verse_data["next_due"]}

if __name__ == "__main__":
    import uvicorn
    print("Starting CME Service. Ensure SANCTUM_API_KEY is set.")
    uvicorn.run(app, host="0.0.0.0", port=8000)
