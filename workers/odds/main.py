from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os
import logging

app = FastAPI()
logger = logging.getLogger("uvicorn")

class OddsRequest(BaseModel):
    race_id: str

@app.post("/analyze_odds")
def analyze_odds(request: OddsRequest):
    logger.info(f"Analyzing odds for: {request.race_id}")
    # Mock data
    return {
        "favorites": ["Equinox (2.1)", "Do Deuce (3.5)"],
        "trend": "Favorites require valid justification."
    }

if __name__ == "__main__":
    port = int(os.getenv("APP_PORT", 8082))
    uvicorn.run(app, host="0.0.0.0", port=port)
