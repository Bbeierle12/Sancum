
import os
import logging
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel, Field
import re
from typing import List, Optional

# Import the modular detectors
from src.detectors import chiastic, golden

# --- Configuration ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = os.getenv("SANCTUM_API_KEY", "dev")
if API_KEY == "dev":
    logger.warning(
        "SANCTUM_API_KEY not set. Running in development mode; requests are not authenticated."
    )

app = FastAPI(
    title="Sanctum Pivot Analyzer Service",
    description="A service to analyze scripture text for structural patterns.",
    version="1.0.0",
)

# --- Pydantic Models ---
class TextToAnalyze(BaseModel):
    text: str = Field(..., min_length=1, description="The scripture text to analyze.")

class ChiasticAnalysis(BaseModel):
    type: str = "Chiastic"
    center: str
    elements: List[str]
    score: float
    match_count: int
    depth: int

class GoldenRatioAnalysis(BaseModel):
    type: str = "Golden Ratio"
    total_words: int
    major_pivot: dict
    minor_pivot: Optional[dict] = None

class AnalysisResponse(BaseModel):
    chiastic: Optional[ChiasticAnalysis] = None
    golden_ratio: Optional[GoldenRatioAnalysis] = None

# --- API Key Dependency ---
async def verify_api_key(x_api_key: str = Header(None)):
    if API_KEY != "dev" and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# --- API Endpoints ---
@app.post("/analyze_text", response_model=AnalysisResponse, dependencies=[Depends(verify_api_key)])
async def perform_analysis(payload: TextToAnalyze):
    """Analyzes text for chiastic and golden ratio patterns."""
    try:
        words = re.findall(r'\b\w+\b', payload.text.lower())
        
        chiastic_result_data = chiastic.detect(words)
        chiastic_response = None
        if chiastic_result_data:
            center_index, score = chiastic_result_data
            # The detector only provides index and score. Other fields are placeholders.
            chiastic_response = ChiasticAnalysis(
                center=words[center_index] if center_index < len(words) else "",
                elements=[],
                score=score,
                match_count=0, # This would require a more advanced detector
                depth=0,       # This would require a more advanced detector
            )

        golden_result_index = golden.detect(words)
        golden_response = None
        if golden_result_index is not None and golden_result_index < len(words):
            minor_pivot_index = len(words) - golden_result_index
            golden_response = GoldenRatioAnalysis(
                total_words=len(words),
                major_pivot={"index": golden_result_index, "word": words[golden_result_index]},
                minor_pivot={"index": minor_pivot_index, "word": words[minor_pivot_index]} if minor_pivot_index < len(words) and minor_pivot_index >= 0 else None,
            )

        return AnalysisResponse(
            chiastic=chiastic_response, 
            golden_ratio=golden_response
        )
    except Exception as e:
        logger.error(f"An unhandled error occurred during text analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Pivot Analyzer Service on http://0.0.0.0:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)
