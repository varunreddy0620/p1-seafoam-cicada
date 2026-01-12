# app/graph/nodes.py
import httpx
import re
import os
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from .state import TriageState

# Base URL for existing mock API
API_BASE = "http://localhost:8000"

def get_llm():
    """Lazy load LLM to ensure env vars are loaded"""
    return ChatOpenAI(model="gpt-4o-mini", temperature=0)

def ingest_node(state: TriageState) -> dict:
    """Extract ticket text from last user message"""
    last_msg = state["messages"][-1]
    return {
        "ticket_text": last_msg.content
    }

def classify_issue_node(state: TriageState) -> dict:
    """
    Classify issue and extract order_id
    Uses existing /classify/issue endpoint
    """
    ticket = state["ticket_text"]
    
    # Extract order_id if not already provided
    order_id = state.get("order_id")
    if not order_id:
        match = re.search(r'(ORD\d{4})', ticket, re.IGNORECASE)
        if match:
            order_id = match.group(1).upper()
    
    # Call existing classification API
    try:
        response = httpx.post(
            f"{API_BASE}/classify/issue",
            json={"ticket_text": ticket},
            timeout=5.0
        )
        if response.status_code == 200:
            data = response.json()
            issue_type = data.get("issue_type", "unknown")
        else:
            issue_type = "unknown"
    except Exception as e:
        print(f"Classification API error: {e}")
        issue_type = "unknown"
    
    return {
        "order_id": order_id,
        "issue_type": issue_type
    }

def fetch_order_node(state: TriageState) -> dict:
    """
    Fetch order details from /orders/get endpoint
    This is a ToolNode - only called if order_id exists
    """
    order_id = state.get("order_id")
    
    if not order_id:
        return {"evidence": {"error": "No order_id available"}}
    
    try:
        response = httpx.get(
            f"{API_BASE}/orders/get",
            params={"order_id": order_id},
            timeout=5.0
        )
        
        if response.status_code == 200:
            order_data = response.json()
            return {"evidence": order_data}
        else:
            return {"evidence": {"error": f"Order {order_id} not found"}}
            
    except Exception as e:
        return {"evidence": {"error": str(e)}}

def draft_reply_node(state: TriageState) -> dict:
    """
    Draft reply using /reply/draft endpoint
    """
    issue_type = state.get("issue_type")
    order_data = state.get("evidence", {})
    ticket = state.get("ticket_text", "")
    
    # Call existing reply API
    try:
        response = httpx.post(
            f"{API_BASE}/reply/draft",
            json={
                "issue_type": issue_type,
                "order": order_data,
                "ticket_text": ticket
            },
            timeout=5.0
        )
        
        if response.status_code == 200:
            reply = response.json().get("reply_text", "")
        else:
            reply = f"We are reviewing your request for order {state.get('order_id', 'N/A')}."
    except Exception as e:
        reply = f"We are reviewing your request for order {state.get('order_id', 'N/A')}."
    
    # Use the reply directly
    return {
        "recommendation": reply,
        "messages": [AIMessage(content=reply)]
    }
