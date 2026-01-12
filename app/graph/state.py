# app/graph/state.py
from typing import TypedDict, Annotated, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class TriageState(TypedDict):
    """State schema for ticket triage workflow"""
    messages: Annotated[list[BaseMessage], add_messages]
    ticket_text: str
    order_id: Optional[str]
    issue_type: Optional[str]
    evidence: Optional[dict]
    recommendation: Optional[str]