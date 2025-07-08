
import os
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel, Field
import re
from typing import List, Optional

# Import the modular detectors
from src.detectors import chiastic, golden

# --- Configuration ---
API_KEY = os.getenv("SANCTUM_API_KEY")
if not API_KEY:
    raise ValueError("SANCTUM_API_KEY environment variable not set.")

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
    major_pivot_index: int

class AnalysisResponse(BaseModel):
    chiastic: Optional[ChiasticAnalysis] = None
    golden_ratio: Optional[GoldenRatioAnalysis] = None

# --- API Key Dependency ---
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# --- API Endpoints ---
@app.post("/analyze_text", response_model=AnalysisResponse, dependencies=[Depends(verify_api_key)])
async def perform_analysis(payload: TextToAnalyze):
    """Analyzes text for chiastic and golden ratio patterns."""
    try:
        words = re.findall(r'\b\w+\b', payload.text.lower())
        
        chiastic_result = chiastic.detect(words)
        
        golden_result = None
        major_pivot_index = golden.detect(words)
        if major_pivot_index is not None:
            golden_result = GoldenRatioAnalysis(
                total_words=len(words),
                major_pivot_index=major_pivot_index
            )

        return AnalysisResponse(
            chiastic=chiastic_result, 
            golden_ratio=golden_result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("Starting Pivot Analyzer Service. Ensure SANCTUM_API_KEY is set.")
    uvicorn.run(app, host="0.0.0.0", port=8001)
