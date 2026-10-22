# Meeting-to-Tasks Agent 🤖

> **Agentic AI Hackathon 2026** • Powered by **Ziro.Digital**  
> **Domain:** Industry / Business & Productivity AI  
> **Problem Statement:** Meeting-to-Tasks Agent  
> **Official Demo Target:** Trello Free Board

---

## 🎯 What This Agent Does
After a call or meeting, the agent turns the raw transcript and team roster into owned, dated cards on a team's Trello board, adhering strictly to safe human approval gates, ambiguity disambiguation, tentative filtering, and independent verification.

### 5-Step Workflow Pipeline:
1. **01 Collect Details:** Parses meeting transcript and team member roster with stable IDs.
2. **02 Plan Next Steps:** Extracts confirmed decisions, filters tentative items (`maybe`, `perhaps`), and identifies owners.
3. **03 Query Board:** Connects to Trello board (`My Trello board` ➔ `This Week`).
4. **04 Take Action (Human Approval):** Presents proposed cards with owner, due date, and transcript evidence; prompts approval before touching Trello.
5. **05 Independent Verification:** Re-reads created Trello cards via REST API to verify owner match, due date match, and transcript link integrity.

---

## 🧪 4 Official Test Cases (100% Passing)

| Test Case | Scenario | Expected Behavior | Agent Output & Evidence | Status |
|---|---|---|---|---|
| **TC1** | Clear decision with owner & date | Correct Trello card created with owner, date, and link to transcript | Extracted task for Rahul & Siddharth. Approved and created card on Trello list `This Week`. Step 5 verification passed. | `PASS` ✅ |
| **TC2** | Two team members named Priya | Detects ambiguous owner, prompts clarification ("Which one?") | Flagged ambiguity: *"Two team members found matching 'Priya'. Did you mean Priya Sharma (Backend Engineer) or Priya Patel (UI/UX Designer)?"*. 0 cards created until resolved. | `PASS` ✅ |
| **TC3** | 'Maybe next week' | Left as tentative, no card created on Trello | Detected tentative markers (`maybe`, `perhaps`). Filtered 2 items as tentative discussions. 0 cards queued. | `PASS` ✅ |
| **TC4** | Same transcript re-imported | Deduplication blocks duplicate cards | SHA-256 content hash matched existing record ID. Prevented duplicate card creation. | `PASS` ✅ |

---

## 🚀 How to Run

### 1. Run Automated Test Suite (Console)
```powershell
python test_cases.py
```
Outputs the official test runner summary: **4/4 PASSING (100% SCORE)**.

### 2. Launch Interactive Web Dashboard
Double-click `start_agent.bat` or run:
```powershell
python server.py
```
Open your browser at: **[http://127.0.0.1:8050](http://127.0.0.1:8050)**

### Web Dashboard Features:
- **1-Click Test Scenarios (TC1 - TC4):** Buttons to load and test each hackathon scenario instantly.
- **Ambiguity Resolver (TC2):** Interactive choice to select between multiple members with the same name.
- **Human Approval Gate (Step 04):** Review proposed card details with transcript quote before pushing.
- **Live Verification Inspector (Step 05):** Real-time API audit verifying owner, due date, and transcript quote match.
- **Live Trello Board Viewer:** Displays synced cards on your Trello board in real time.
