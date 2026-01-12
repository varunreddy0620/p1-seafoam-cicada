# tests/test_workflow.py
import pytest
from langchain_core.messages import HumanMessage
from app.graph.workflow import build_graph

def test_full_workflow_with_order_id():
    """Test complete workflow with order_id in text"""
    graph = build_graph()
    
    result = graph.invoke({
        "messages": [HumanMessage(content="I'd like a refund for order ORD1001. The mouse is not working.")]
    })
    
    assert result["order_id"] == "ORD1001"
    assert result["issue_type"] is not None
    assert result["recommendation"] is not None

def test_order_id_extraction():
    """Test that order_id is extracted from text"""
    graph = build_graph()
    
    result = graph.invoke({
        "messages": [HumanMessage(content="My order ORD1002 hasn't arrived yet")]
    })
    
    assert result["order_id"] == "ORD1002"
    assert result["issue_type"] is not None

def test_no_order_id():
    """Test workflow when no order_id is present"""
    graph = build_graph()
    
    result = graph.invoke({
        "messages": [HumanMessage(content="I need help with my account")]
    })
    
    assert result["order_id"] is None
    assert result["recommendation"] is not None