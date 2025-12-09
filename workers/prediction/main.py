from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os
import logging

app = FastAPI()
logger = logging.getLogger("uvicorn")

class PredictionRequest(BaseModel):
    race_id: str

@app.post("/predict")
def predict(request: PredictionRequest):
    logger.info(f"Generating prediction for: {request.race_id}")
    # Mock data
    return {
        "winner": "Equinox",
        "confidence": "High",
        "reasoning": "Strong performance in fetch_data and odds analysis."
    }

if __name__ == "__main__":
    port = int(os.getenv("APP_PORT", 8083))
    uvicorn.run(app, host="0.0.0.0", port=port)
