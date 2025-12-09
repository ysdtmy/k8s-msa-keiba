from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os
import logging

app = FastAPI()
logger = logging.getLogger("uvicorn")

class RaceDataRequest(BaseModel):
    race_id: str

@app.post("/get_race_data")
def get_race_data(request: RaceDataRequest):
    logger.info(f"Fetching race data for: {request.race_id}")
    # Mock data
    return {
        "race_name": "Tokyo Yushun (Japanese Derby)",
        "weather": "Sunny",
        "track_condition": "Good",
        "horses": ["Do Deuce", "Equinox", "Ask Victor More"]
    }

if __name__ == "__main__":
    port = int(os.getenv("APP_PORT", 8081))
    uvicorn.run(app, host="0.0.0.0", port=port)
