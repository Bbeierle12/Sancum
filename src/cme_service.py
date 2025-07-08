
import os
import sqlite_utils
import json
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Import the algorithm module
from src.algorithms.sm2 import update_sm2

# --- Configuration ---
API_KEY = os.getenv("SANCTUM_API_KEY")
if not API_KEY:
    raise ValueError("SANCTUM_API_KEY environment variable not set.")

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'sanctum.db')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


# --- Pydantic Models (DTOs) ---
class Verse(BaseModel):
    verse_id: str = Field(..., description="Canonical verse reference, e.g., 'John_3_16'")
    text: str = Field(..., description="The full text of the scripture.")
    covenant_tags: Optional[List[str]] = []
    emotion_codes: Optional[List[str]] = []
    notes: Optional[str] = ""
    # SM-2 Spaced Repetition Fields
    repetitions: int = 0
    easiness_factor: float = 2.5
    interval: int = 0  # in days
    next_due: datetime = Field(default_factory=datetime.utcnow)


class VerseUpdate(BaseModel):
    quality: int = Field(..., ge=0, le=4, description="Recall quality: 0-Again, 1-Hard, 2-Good, 3-Easy, 4-Perfect")


# --- Database Setup ---
def get_db():
    db = sqlite_utils.Database(DB_PATH)
    if "verses" not in db.table_names():
        db["verses"].create({
            "verse_id": str,
            "text": str,
            "covenant_tags": str,  # Stored as JSON string
            "emotion_codes": str,  # Stored as JSON string
            "notes": str,
            "repetitions": int,
            "easiness_factor": float,
            "interval": int,
            "next_due": datetime,
        }, pk="verse_id")
        print("Database table 'verses' created.")
    return db

# --- Service Class ---
class CMEService:
    """
    Orchestrating service layer for the Covenant Memory Engine.
    Coordinates all workflows related to covenantal memory practice.
    """
    def __init__(self, db: sqlite_utils.Database):
        self.db = db

    def add_verse(self, verse: Verse):
        """
        Persists a new verse to the database, echoing the principle:
        “Write them upon the table of thine heart.” (Prov 3:3 KJV)
        """
        # This method handles both creation and updates (upsert).
        verse_dict = verse.model_dump()
        # Serialize lists to JSON strings for storage
        verse_dict["covenant_tags"] = json.dumps(verse.covenant_tags)
        verse_dict["emotion_codes"] = json.dumps(verse.emotion_codes)
        
        self.db["verses"].upsert(verse_dict, pk="verse_id")
        return {"verse_id": verse.verse_id, "status": "created_or_updated"}

    def get_flashcards(self, limit: int = 10) -> List[Verse]:
        """Retrieves verses that are due for review."""
        now = datetime.utcnow()
        # Using 'lt' because we want anything past due
        due_verses = self.db["verses"].rows_where("next_due < ?", [now.isoformat()], order_by="next_due", limit=limit)
        
        results = []
        for verse_row in due_verses:
            # Deserialize JSON strings back to lists
            if verse_row.get('covenant_tags'):
                verse_row['covenant_tags'] = json.loads(verse_row['covenant_tags'])
            if verse_row.get('emotion_codes'):
                verse_row['emotion_codes'] = json.loads(verse_row['emotion_codes'])
            results.append(Verse(**verse_row))
        return results

    def review_verse(self, verse_id: str, quality: int):
        """
        Records a review for a verse and schedules the next review date,
        practicing line-upon-line recollection.
        """
        try:
            # Fetch the verse from the database
            verse_row = self.db["verses"].get(verse_id)
        except sqlite_utils.db.NotFoundError:
            raise HTTPException(status_code=404, detail="Verse not found")
        
        # Deserialize JSON strings to lists before passing to algorithm
        if verse_row.get('covenant_tags'):
            verse_row['covenant_tags'] = json.loads(verse_row['covenant_tags'])
        if verse_row.get('emotion_codes'):
            verse_row['emotion_codes'] = json.loads(verse_row['emotion_codes'])

        # Apply the SM-2 algorithm to get updated verse data
        updated_verse_data = update_sm2(verse_row, quality)

        # Convert lists back to JSON strings for storage
        updated_verse_data["covenant_tags"] = json.dumps(updated_verse_data["covenant_tags"])
        updated_verse_data["emotion_codes"] = json.dumps(updated_verse_data["emotion_codes"])

        # Update the verse record in the database
        self.db["verses"].update(verse_id, updated_verse_data)
        return {"verse_id": verse_id, "status": "review_recorded", "next_due": updated_verse_data["next_due"]}

# --- FastAPI App ---
app = FastAPI(
    title="Sanctum Covenant Memory Engine (CME)",
    description="A service to manage scripture flashcards with spaced repetition.",
    version="1.0.0",
)

# --- API Key Dependency ---
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# --- Service Dependency ---
def get_cme_service():
    """Dependency injector for the CMEService."""
    db = get_db()
    return CMEService(db)

# --- API Endpoints ---
@app.on_event("startup")
async def startup_event():
    # Ensure the database and table exist on startup
    get_db()

@app.post("/add_verse", status_code=201, dependencies=[Depends(verify_api_key)])
async def add_verse_endpoint(verse: Verse, service: CMEService = Depends(get_cme_service)):
    """Adds a new verse to the memory database."""
    try:
        return service.add_verse(verse)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/flashcards", response_model=List[Verse], dependencies=[Depends(verify_api_key)])
async def get_flashcards_endpoint(limit: int = 10, service: CMEService = Depends(get_cme_service)):
    """Retrieves all verses due for review today."""
    return service.get_flashcards(limit=limit)

@app.post("/review_verse/{verse_id}", status_code=200, dependencies=[Depends(verify_api_key)])
async def review_verse_endpoint(verse_id: str, update: VerseUpdate, service: CMEService = Depends(get_cme_service)):
    """Updates a verse's spaced repetition data after a review."""
    return service.review_verse(verse_id, update.quality)

if __name__ == "__main__":
    import uvicorn
    print("Starting CME Service. Ensure SANCTUM_API_KEY is set.")
    uvicorn.run(app, host="0.0.0.0", port=8000)
