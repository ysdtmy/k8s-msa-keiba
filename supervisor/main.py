from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uvicorn
import os
import logging

# LangGraph関連のインポート
from graph import app as graph_app

app = FastAPI()
logger = logging.getLogger("uvicorn")

class PredictionRequest(BaseModel):
    race_id: str
    context: Optional[Dict[str, Any]] = None

@app.get("/")
def read_root():
    return {"status": "Supervisor Agent is running"}

@app.post("/predict")
async def predict(request: PredictionRequest):
    logger.info(f"Received prediction request for race: {request.race_id}")
    
    # ここでLangGraphを実行
    inputs = {"race_id": request.race_id, "messages": []}
    result = await graph_app.ainvoke(inputs)
    
    return {"prediction": result.get("final_output", "No prediction"), "messages": [str(m) for m in result.get("messages", [])]}

if __name__ == "__main__":
    port = int(os.getenv("APP_PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
