# app/langgraph_main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from langchain_core.messages import HumanMessage
from .graph.workflow import build_graph
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="LangGraph Ticket Triage")

# Setup LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "true")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "ticket-triage-phase1")

# Build the graph
graph = build_graph()

class TriageRequest(BaseModel):
    ticket_text: str
    order_id: Optional[str] = None

class TriageResponse(BaseModel):
    order_id: Optional[str]
    issue_type: Optional[str]
    evidence: Optional[dict]
    recommendation: Optional[str]

@app.post("/triage/invoke")
async def triage_invoke(request: TriageRequest) -> TriageResponse:
    """
    LangGraph-powered ticket triage endpoint
    """
    try:
        # Invoke the graph
        result = graph.invoke({
            "messages": [HumanMessage(content=request.ticket_text)],
            "order_id": request.order_id
        })
        
        return TriageResponse(
            order_id=result.get("order_id"),
            issue_type=result.get("issue_type"),
            evidence=result.get("evidence"),
            recommendation=result.get("recommendation")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok", "service": "langgraph-triage"}