# Phase 1 - Ticket Triage System

Multi-agent LangGraph workflow for automated customer support ticket triage.

## Setup
```bash
# Clone repository
git clone https://github.com/yourusername/p1-seafoam-cicada.git
cd p1-seafoam-cicada

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Run
```bash
# Terminal 1: Mock API
python3 -m uvicorn app.main:app --port 8000

# Terminal 2: LangGraph API
python3 -m uvicorn app.langgraph_main:app --port 8001
```

## Test
```bash
# Test with curl
curl -X POST http://localhost:8001/triage/invoke \
  -H "Content-Type: application/json" \
  -d '{"ticket_text": "I want a refund for order ORD1001. Mouse is broken."}'

# Run tests
python3 -m pytest tests/ -v
```

## Architecture

### Three-Entity System
1. **Customer** - Submits support tickets
2. **Assistant (AI)** - Classifies, fetches data, drafts responses
3. **Admin** - Reviews and approves (simulated)

### LangGraph Workflow
```
Customer Input 
    ↓
[ingest] → Extract ticket text
    ↓
[classify_issue] → Extract order_id + classify issue type
    ↓
[conditional] → Has order_id?
    ├─ YES → [fetch_order] → Get order data
    └─ NO ─────────────────┐
                           ↓
                   [draft_reply] → Generate response
                           ↓
                         [END]
```

### State Schema
- `messages`: Conversation history
- `ticket_text`: Customer's message
- `order_id`: Extracted order ID
- `issue_type`: Classified category
- `evidence`: Order data from API
- `recommendation`: Draft response

## AI Tool Usage

I used **Cursor AI** to accelerate development:

1. **Boilerplate Generation** - Generated FastAPI and LangGraph structure (saved ~25 min)
2. **Node Implementation** - Helped structure async API calls with error handling
3. **Test Creation** - Generated comprehensive test cases covering edge cases
4. **Debugging** - Assisted with Python 3.9 compatibility issues and state management
5. **Documentation** - Created README structure and inline comments

**Time Breakdown:**
- Total: ~90 minutes
- Manual planning: 10 min (no AI)
- Implementation with AI: 60 min
- Testing & debugging: 15 min
- Documentation: 5 min

**Key Insight:** AI saved ~40% of time on boilerplate, allowing me to focus on workflow design and integration logic.

## Project Structure
```
p1-seafoam-cicada/
├── app/
│   ├── main.py              # Mock API
│   ├── langgraph_main.py    # LangGraph FastAPI
│   └── graph/
│       ├── state.py         # State schema
│       ├── nodes.py         # Node implementations
│       └── workflow.py      # Graph builder
├── tests/
│   └── test_workflow.py     # Tests
├── mock_data/               # Mock orders, issues, replies
├── .github/workflows/       # CI configuration
└── requirements.txt
```

## Demo Video

🎥 [Watch Loom Demo](https://www.loom.com/share/8061a6a37992474b86fc2582ed9a1f5b)

## License
MIT
