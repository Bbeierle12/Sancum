
import os
from fastapi import FastAPI, Depends, HTTPException, Header
import re
from typing import List

# Import the schemas
from src.schemas import PivotIn, PivotOut, PivotPoint, ForecastRequest, ForecastPoint
from src.forecasters.hawkes import HawkesForecaster

# Import the modular detectors
from src.detectors import chiastic, golden

# --- Configuration ---
API_KEY = os.getenv("SANCTUM_API_KEY")
if not API_KEY:
    raise ValueError("SANCTUM_API_KEY environment variable not set.")

app = FastAPI(
    title="Sanctum Pivot Analyzer Service",
    description="A service to analyze scripture text for structural patterns and forecast events.",
    version="1.2.0",
)

# --- API Key Dependency ---
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# --- Dummy Data for Forecaster ---
# In a real system, this would come from a user event database.
DUMMY_USER_EVENTS = {
    "u1": [1, 2, 5, 8, 12, 13],
    "u2": [3, 7, 9],
}

# --- API Endpoints ---
@app.post("/analyze_text", response_model=List[PivotOut], dependencies=[Depends(verify_api_key)])
async def perform_analysis(payload: PivotIn) -> List[PivotOut]:
    """Analyzes text for chiastic and golden ratio patterns based on selected lenses."""
    try:
        tokens = re.findall(r'\b\w+\b', payload.text_section.lower())
        points: List[PivotPoint] = []

        if "CHIASMUS" in payload.lens:
            res = chiastic.detect(tokens)
            if res:
                points.append(
                    PivotPoint(detector="chiastic", position=res[0], score=res[1])
                )
        
        if "GOLDEN" in payload.lens:
            idx = golden.detect(tokens)
            if idx is not None:
                points.append(PivotPoint(detector="golden", position=idx, score=1.0))
        
        pivot_result = PivotOut(
            text_section=payload.text_section,
            scale=payload.scale,
            points=points
        )
        
        return [pivot_result]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/forecast", response_model=List[ForecastPoint], dependencies=[Depends(verify_api_key)])
async def forecast_events(req: ForecastRequest) -> List[ForecastPoint]:
    """
    Forecasts the probability of a pivot event for a user over a given horizon.
    """
    try:
        # Get historical events for the user (using dummy data for now)
        events = DUMMY_USER_EVENTS.get(req.user_id, [])

        # Initialize and run the forecaster
        forecaster = HawkesForecaster()
        probabilities = forecaster.forecast(events=events, horizon=req.horizon)
        
        # Format the response
        response = [
            ForecastPoint(timestep=i + 1, probability=prob)
            for i, prob in enumerate(probabilities)
        ]
        return response
    except Exception as e:
        # In a real app, you'd have more specific error handling
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    print("Starting Pivot Analyzer Service. Ensure SANCTUM_API_KEY is set.")
    uvicorn.run(app, host="0.0.0.0", port=8001)
