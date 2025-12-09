from typing import TypedDict, Annotated, Sequence, Union, Literal
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
import operator
import requests
import os
import logging
import json

logger = logging.getLogger("uvicorn")

# --- Dapr Client ---
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", 3500)
DAPR_BASE_URL = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/invoke"

def call_dapr_service(app_id: str, method: str, data: dict) -> dict:
    url = f"{DAPR_BASE_URL}/{app_id}/method/{method}"
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to call {app_id}: {e}")
        return {"error": str(e)}

# --- Define Tools ---

@tool
def get_race_data(race_id: str):
    """Fetches race data given a race_id."""
    return call_dapr_service("worker-race-data", "get_race_data", {"race_id": race_id})

@tool
def analyze_odds(race_id: str):
    """Analyzes odds for a given race_id. Should be called after fetching race data."""
    return call_dapr_service("worker-odds", "analyze_odds", {"race_id": race_id})

@tool
def predict_race(race_id: str):
    """Makes a final prediction for the race. Should be called after odds analysis."""
    return call_dapr_service("worker-prediction", "predict", {"race_id": race_id})

TOOLS = [get_race_data, analyze_odds, predict_race]
TOOL_NODE = ToolNode(TOOLS)

# --- State Definition ---

class AgentState(TypedDict):
    race_id: str
    messages: Annotated[Sequence[BaseMessage], operator.add]
    final_output: dict

# --- Nodes ---

def supervisor_node(state: AgentState):
    """
    Simulates a supervisor agent that decides which tool to call next based on the conversation history.
    Since we don't have a real LLM, we implement a simple state machine logic here.
    """
    messages = state["messages"]
    race_id = state["race_id"]
    
    logger.info(f"Supervisor processing. History len: {len(messages)}")

    # Check the last message to decide next step
    last_message = messages[-1] if messages else None
    
    # Initial state or after a ToolMessage
    if not last_message or isinstance(last_message, ToolMessage):
        # Decide next action based on what tools have been called
        tool_names_called = [
            m.name for m in messages 
            if isinstance(m, ToolMessage)
        ]
        
        if "get_race_data" not in tool_names_called:
            logger.info("Decided to call: get_race_data")
            return {
                "messages": [
                    AIMessage(
                        content="",
                        tool_calls=[{
                            "name": "get_race_data",
                            "args": {"race_id": race_id},
                            "id": "call_race_data"
                        }]
                    )
                ]
            }
            
        elif "analyze_odds" not in tool_names_called:
            logger.info("Decided to call: analyze_odds")
            return {
                "messages": [
                    AIMessage(
                        content="",
                        tool_calls=[{
                            "name": "analyze_odds",
                            "args": {"race_id": race_id},
                            "id": "call_analyze_odds"
                        }]
                    )
                ]
            }
            
        elif "predict_race" not in tool_names_called:
            logger.info("Decided to call: predict_race")
            return {
                "messages": [
                    AIMessage(
                        content="",
                        tool_calls=[{
                            "name": "predict_race",
                            "args": {"race_id": race_id},
                            "id": "call_predict_race"
                        }]
                    )
                ]
            }
            
        else:
            # All tools called, finish
            logger.info("All tools called. Finishing.")
            # Extract prediction from the last tool result
            last_tool_result = json.loads(last_message.content) if last_message else {}
            return {"final_output": last_tool_result}
    
    return {}

# --- Graph Construction ---

workflow = StateGraph(AgentState)

workflow.add_node("supervisor", supervisor_node)
workflow.add_node("tools", TOOL_NODE)

workflow.add_edge(START, "supervisor")

def should_continue(state: AgentState) -> Literal["tools", END]:
    messages = state["messages"]
    last_message = messages[-1]
    
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"
    return END

workflow.add_conditional_edges(
    "supervisor",
    should_continue,
)

workflow.add_edge("tools", "supervisor")

app = workflow.compile()
