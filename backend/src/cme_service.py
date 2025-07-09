
import os
import logging
import sqlite_utils
import json
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Import the algorithm module
from src.algorithms.sm2 import update_sm2

# --- Configuration ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = os.getenv("SANCTUM_API_KEY", "dev")
if API_KEY == "dev":
    logger.warning(
        "SANCTUM_API_KEY not set. Running in development mode; requests are not authenticated."
    )

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'sanctum.db')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


# --- Pydantic Models (DTOs) ---
class Pivot(BaseModel):
    type: str
    center: Optional[str] = None
    elements: Optional[List[str]] = []
    score: Optional[float] = None
    match_count: Optional[int] = None
    depth: Optional[int] = None
    total_words: Optional[int] = None
    major_pivot: Optional[dict] = None
    minor_pivot: Optional[dict] = None

class Verse(BaseModel):
    verse_id: str = Field(..., description="Canonical verse reference, e.g., 'John_3_16'")
    text: str = Field(..., description="The full text of the scripture.")
    covenant_tags: Optional[List[str]] = []
    emotion_codes: Optional[List[str]] = []
    notes: Optional[str] = ""
    pivot: Optional[Pivot] = None
    # SM-2 Spaced Repetition Fields (for general, non-user-specific reviews)
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
            "pivot": str,          # Stored as JSON string
            "repetitions": int,
            "easiness_factor": float,
            "interval": int,
            "next_due": datetime,
        }, pk="verse_id")
        logger.info("Database table 'verses' created.")
    # Simple migration: add pivot column if it doesn't exist
    elif "pivot" not in db["verses"].columns_dict:
        db["verses"].add_column("pivot", str)
        logger.info("Column 'pivot' added to 'verses' table.")
    
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
        verse_dict["pivot"] = json.dumps(verse.pivot.model_dump()) if verse.pivot else None
        
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
            
            pivot_data = verse_row.get('pivot')
            if pivot_data and pivot_data != 'null':
                verse_row['pivot'] = Pivot(**json.loads(pivot_data))
            else:
                verse_row['pivot'] = None
                
            results.append(Verse(**verse_row))
        return results

    def review_verse(self, verse_id: str, quality: int):
        """
        Records a review for a verse and schedules the next review date,
        practicing line-upon-line recollection.
        This is a legacy, non-user-specific review endpoint.
        """
        try:
            # Fetch the verse from the database
            verse_row = self.db["verses"].get(verse_id)
        except sqlite_utils.NotFoundError:
            raise HTTPException(status_code=404, detail="Verse not found")
        
        updated_verse_data = update_sm2(verse_row, quality)

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
async def verify_api_key(x_api_key: str = Header(None)):
    if API_KEY != "dev" and x_api_key != API_KEY:
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
    """(Legacy) Updates a verse's spaced repetition data after a review."""
    return service.review_verse(verse_id, update.quality)

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting CME Service on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
