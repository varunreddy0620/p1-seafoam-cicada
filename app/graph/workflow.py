# app/graph/workflow.py
from langgraph.graph import StateGraph, END
from .state import TriageState
from .nodes import (
    ingest_node,
    classify_issue_node,
    fetch_order_node,
    draft_reply_node
)

def should_fetch_order(state: TriageState) -> str:
    """
    Conditional edge: only fetch order if order_id exists
    """
    if state.get("order_id"):
        return "fetch_order"
    return "draft_reply"

def build_graph():
    """Build and compile the LangGraph workflow"""
    
    # Initialize the graph with state schema
    workflow = StateGraph(TriageState)
    
    # Add all nodes
    workflow.add_node("ingest", ingest_node)
    workflow.add_node("classify_issue", classify_issue_node)
    workflow.add_node("fetch_order", fetch_order_node)
    workflow.add_node("draft_reply", draft_reply_node)
    
    # Define the flow
    workflow.set_entry_point("ingest")
    workflow.add_edge("ingest", "classify_issue")
    
    # Conditional edge: fetch order only if order_id exists
    workflow.add_conditional_edges(
        "classify_issue",
        should_fetch_order,
        {
            "fetch_order": "fetch_order",
            "draft_reply": "draft_reply"
        }
    )
    
    # Connect fetch_order to draft_reply
    workflow.add_edge("fetch_order", "draft_reply")
    
    # End after draft_reply
    workflow.add_edge("draft_reply", END)
    
    # Compile the graph
    return workflow.compile()