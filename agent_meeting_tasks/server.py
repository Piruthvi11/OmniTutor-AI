from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from pathlib import Path
from agent_core import MeetingTasksAgent
from trello_service import TrelloService
from config import TRELLO_DEFAULT_LIST_ID, TRELLO_BOARD_ID

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Meeting-to-Tasks Agent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = MeetingTasksAgent()
trello = TrelloService()

class AnalyzeRequest(BaseModel):
    transcript_id: str = "MEET-001"
    transcript_text: str
    team_members: List[Dict[str, str]]

class ApproveRequest(BaseModel):
    task: Dict[str, Any]
    transcript_url: str = ""

@app.get("/api/status")
def get_status():
    try:
        lists = trello.get_lists()
        cards = trello.get_cards_in_list(TRELLO_DEFAULT_LIST_ID)
        return {
            "status": "CONNECTED",
            "board_id": TRELLO_BOARD_ID,
            "target_list_id": TRELLO_DEFAULT_LIST_ID,
            "lists": lists,
            "cards_count": len(cards),
            "recent_cards": cards[:5]
        }
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

@app.post("/api/analyze")
def analyze_transcript(req: AnalyzeRequest):
    try:
        result = agent.process_transcript(
            transcript_id=req.transcript_id,
            transcript_text=req.transcript_text,
            team_members=req.team_members
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/approve")
def approve_and_execute(req: ApproveRequest):
    try:
        result = agent.execute_approved_task(req.task, transcript_url=req.transcript_url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/cards")
def get_cards():
    try:
        cards = trello.get_cards_in_list(TRELLO_DEFAULT_LIST_ID)
        return {"status": "SUCCESS", "cards": cards}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/verify-card/{card_id}")
def verify_card(card_id: str, expected_owner: str = "", expected_date: str = "", expected_ref: str = ""):
    try:
        res = trello.verify_card(
            card_id=card_id,
            expected_owner=expected_owner,
            expected_date=expected_date or None,
            expected_transcript_ref=expected_ref or "transcript"
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reset-db")
def reset_database():
    try:
        with agent._get_connection() as conn:
            conn.execute("DELETE FROM processed_transcripts")
            conn.execute("DELETE FROM tasks")
            conn.execute("DELETE FROM items_audit")
            conn.commit()
        return {"status": "SUCCESS", "message": "Database records cleared for clean test runs."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/test-scenario/{scenario_id}")
def get_test_scenario(scenario_id: str):
    scenarios = {
        "TC1": {
            "title": "TC1: Clear Decision with Owner & Date",
            "transcript_id": "TC1-SPRINT-001",
            "transcript": "Sneha: Good morning team. Let's confirm sprint action items.\nRahul will deploy the authentication module by Friday.\nSiddharth will configure the production database cluster by Monday.",
            "team": [
                {"name": "Rahul Verma", "role": "Frontend Lead", "email": "rahul@company.com"},
                {"name": "Siddharth Rao", "role": "DevOps Engineer", "email": "siddharth@company.com"},
                {"name": "Sneha Reddy", "role": "Product Manager", "email": "sneha@company.com"}
            ],
            "expected": "Extracts confirmed decisions with owners & due dates. Creates cards on Trello with link after approval."
        },
        "TC2": {
            "title": "TC2: Two Team Members Named Priya",
            "transcript_id": "TC2-CHECKOUT-001",
            "transcript": "Arun: We reviewed customer feedback on checkout.\nPriya will redesign the payment gateway interface by Wednesday.",
            "team": [
                {"name": "Priya Sharma", "role": "Backend Engineer", "email": "priya.sharma@company.com"},
                {"name": "Priya Patel", "role": "UI/UX Designer", "email": "priya.patel@company.com"},
                {"name": "Arun Kumar", "role": "Tech Lead", "email": "arun@company.com"}
            ],
            "expected": "Ambiguity detected: Asks user which Priya was intended before any card is created."
        },
        "TC3": {
            "title": "TC3: 'Maybe Next Week' (Tentative Item)",
            "transcript_id": "TC3-PLANNING-001",
            "transcript": "Sneha: We looked at the analytics report.\nMaybe next week we could explore adding Google Pay support.\nPerhaps we might migrate our image hosting later.",
            "team": [
                {"name": "Rahul Verma", "role": "Frontend Lead", "email": "rahul@company.com"},
                {"name": "Sneha Reddy", "role": "Product Manager", "email": "sneha@company.com"}
            ],
            "expected": "Classified as tentative discussion items. Left without creating Trello cards."
        },
        "TC4": {
            "title": "TC4: Same Transcript Re-imported (Deduplication)",
            "transcript_id": "TC4-REIMPORT-001",
            "transcript": "Sneha: Good morning team. Let's confirm sprint action items.\nRahul will deploy the authentication module by Friday.\nSiddharth will configure the production database cluster by Monday.",
            "team": [
                {"name": "Rahul Verma", "role": "Frontend Lead", "email": "rahul@company.com"},
                {"name": "Siddharth Rao", "role": "DevOps Engineer", "email": "siddharth@company.com"}
            ],
            "expected": "Deduplication triggered: SHA-256 content hash matches existing record. Blocks duplicate Trello cards."
        }
    }
    if scenario_id.upper() in scenarios:
        return scenarios[scenario_id.upper()]
    raise HTTPException(status_code=404, detail="Scenario not found")

app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8050, reload=True)
