
import os
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel, Field
import re
from typing import List, Optional

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
    text: str = Field(..., min_length=10, description="The scripture text to analyze.")

class ChiasticAnalysis(BaseModel):
    type: str = "Chiastic"
    center: str
    elements: List[str]

class GoldenRatioAnalysis(BaseModel):
    type: str = "Golden Ratio"
    pivot_word_index: int
    pivot_word: str
    total_words: int

class AnalysisResponse(BaseModel):
    chiastic: Optional[ChiasticAnalysis] = None
    golden_ratio: Optional[GoldenRatioAnalysis] = None

# --- API Key Dependency ---
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# --- Analysis Logic ---
def analyze_text(text: str) -> AnalysisResponse:
    words = re.findall(r'\b\w+\b', text.lower())
    word_count = len(words)
    
    if word_count < 5:
        return AnalysisResponse()

    # Simple Chiastic Heuristic
    center_index = word_count // 2
    chiastic_center = words[center_index]
    chiastic_elements = []
    for i in range(center_index):
        if (word_count - 1 - i) < word_count:
             chiastic_elements.append(f"{words[i]} <-> {words[word_count - 1 - i]}")

    chiastic_result = ChiasticAnalysis(
        center=chiastic_center,
        elements=chiastic_elements
    )

    # Golden Ratio Heuristic
    golden_ratio = 1.61803398875
    pivot_index = round(word_count / golden_ratio)
    golden_pivot_word = words[pivot_index] if 0 <= pivot_index < word_count else ""

    golden_result = GoldenRatioAnalysis(
        pivot_word_index=pivot_index,
        pivot_word=golden_pivot_word,
        total_words=word_count
    )

    return AnalysisResponse(chiastic=chiastic_result, golden_ratio=golden_result)

# --- API Endpoints ---
@app.post("/analyze_text", response_model=AnalysisResponse, dependencies=[Depends(verify_api_key)])
async def perform_analysis(payload: TextToAnalyze):
    """Analyzes text for chiastic and golden ratio patterns."""
    try:
        analysis = analyze_text(payload.text)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("Starting Pivot Analyzer Service. Ensure SANCTUM_API_KEY is set.")
    uvicorn.run(app, host="0.0.0.0", port=8001)
