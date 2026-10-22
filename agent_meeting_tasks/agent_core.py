import re
import hashlib
import sqlite3
import datetime
from typing import Dict, Any, List, Tuple
from config import DB_PATH, TRELLO_DEFAULT_LIST_ID
from trello_service import TrelloService

class MeetingTasksAgent:
    def __init__(self, db_path: str = str(DB_PATH)):
        self.db_path = db_path
        self.trello = TrelloService()
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS processed_transcripts (
                    id TEXT PRIMARY KEY,
                    content_hash TEXT UNIQUE,
                    transcript_text TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    transcript_id TEXT,
                    title TEXT,
                    owner TEXT,
                    due_date TEXT,
                    quote TEXT,
                    status TEXT, -- 'PENDING_APPROVAL', 'APPROVED', 'REJECTED', 'EXECUTED'
                    trello_card_id TEXT,
                    trello_url TEXT,
                    verified INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS items_audit (
                    id TEXT PRIMARY KEY,
                    transcript_id TEXT,
                    item_type TEXT, -- 'CONFIRMED_TASK', 'TENTATIVE_ITEM', 'AMBIGUOUS_OWNER'
                    text TEXT,
                    reason TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def compute_hash(self, text: str) -> str:
        return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()

    def check_duplicate_transcript(self, transcript_text: str) -> Tuple[bool, str]:
        """
        TC4 Check:
        Detects if this exact transcript has already been processed and imported.
        """
        chash = self.compute_hash(transcript_text)
        with self._get_connection() as conn:
            row = conn.execute("SELECT id FROM processed_transcripts WHERE content_hash = ?", (chash,)).fetchone()
            if row:
                return True, row["id"]
        return False, ""

    def process_transcript(self, transcript_id: str, transcript_text: str, team_members: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Main Agent Decision Rules Engine:
        01. Validates inputs & checks deduplication (TC4)
        02. Separates confirmed decisions vs tentative items (TC3)
        03. Resolves owners & detects ambiguous names (TC2)
        04. Prepares confirmed items for human approval (TC1)
        """
        # Step 1: Check duplicate (TC4 Rule)
        is_dup, existing_id = self.check_duplicate_transcript(transcript_text)
        if is_dup:
            return {
                "status": "DUPLICATE_DETECTED",
                "transcript_id": existing_id,
                "message": "Duplicate transcript detected. This meeting has already been imported. No duplicate Trello cards will be created.",
                "created_tasks": [],
                "unresolved_items": [],
                "clarifications_needed": [],
                "evidence": f"Content SHA-256 hash matched existing record ID: {existing_id}"
            }

        # Save transcript to DB
        chash = self.compute_hash(transcript_text)
        with self._get_connection() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO processed_transcripts (id, content_hash, transcript_text) VALUES (?, ?, ?)",
                (transcript_id, chash, transcript_text)
            )
            conn.commit()

        # Step 2 & 3: Parse sentences / action items
        lines = [line.strip() for line in transcript_text.split("\n") if line.strip()]
        
        tentative_patterns = [
            r"\bmaybe\b", r"\bperhaps\b", r"\bmight\b", r"\bwe could\b", r"\bwe should consider\b",
            r"\bthink about\b", r"\btentatively\b", r"\bif possible\b", r"\bnext week maybe\b",
            r"\bpossibly\b", r"\bnot sure yet\b"
        ]

        action_verbs = [
            "deploy", "build", "create", "fix", "update", "send", "review", "test", 
            "prepare", "write", "finish", "complete", "schedule", "design", "publish"
        ]

        confirmed_tasks = []
        tentative_items = []
        clarifications_needed = []

        # Build name lookup dictionary for disambiguation
        # Maps first_name -> list of member dicts
        name_lookup: Dict[str, List[Dict[str, str]]] = {}
        for m in team_members:
            fname = m["name"].split()[0].lower()
            name_lookup.setdefault(fname, []).append(m)

        task_counter = 1
        for line in lines:
            line_clean = line.strip()
            line_lower = line_clean.lower()

            # Rule A: Tentative Check (TC3 Rule)
            is_tentative = any(re.search(pat, line_lower) for pat in tentative_patterns)
            if is_tentative:
                tentative_items.append({
                    "id": f"{transcript_id}-TENT-{task_counter}",
                    "quote": line_clean,
                    "reason": "Contains tentative language ('maybe' / 'consider'). Left as discussion item without creating a Trello card."
                })
                task_counter += 1
                continue

            # Check if this line is an actual assignment/decision
            # Standard task assignment indicators: "will [verb]", "to [verb]", "should [verb]", "assigned to", "needs to"
            is_action_line = any(marker in line_lower for marker in [" will ", " to ", " should ", " assigned to ", " needs to ", " shall "])
            has_action_verb = any(v in line_lower for v in action_verbs)
            
            if not (is_action_line and has_action_verb):
                # Informational speech, greeting, or status update -> not a new task
                continue

            # Strip speaker prefix if present (e.g., "Sneha: Rahul will deploy..." -> action is Rahul deploying)
            action_content = line_clean
            if ":" in line_clean:
                parts = line_clean.split(":", 1)
                # If the part after ':' contains an action, evaluate that part
                if any(marker in parts[1].lower() for marker in [" will ", " to ", " should ", " assigned to "]):
                    action_content = parts[1].strip()

            action_content_lower = action_content.lower()

            # Rule B: Owner Identification & Ambiguity Check (TC2 Rule)
            detected_first_names = []
            for fname in name_lookup:
                if re.search(rf"\b{fname}\b", action_content_lower):
                    detected_first_names.append(fname)

            if not detected_first_names:
                tentative_items.append({
                    "id": f"{transcript_id}-UNASSIGNED-{task_counter}",
                    "quote": line_clean,
                    "reason": "Action item mentioned but no assigned owner from the team roster was found."
                })
                task_counter += 1
                continue

            # Process detected owner(s)
            for fname in detected_first_names:
                matching_members = name_lookup[fname]

                # TC2: Multiple members with same name -> Request Clarification
                if len(matching_members) > 1:
                    options_str = " or ".join([f"{m['name']} ({m.get('role', 'Member')})" for m in matching_members])
                    clarifications_needed.append({
                        "id": f"{transcript_id}-AMBIG-{task_counter}",
                        "name_searched": fname.capitalize(),
                        "matching_candidates": matching_members,
                        "question": f"Two team members found matching '{fname.capitalize()}'. Did you mean {options_str}?",
                        "quote": line_clean,
                        "reason": f"Ambiguous owner: '{fname.capitalize()}' matches multiple team members: {options_str}."
                    })
                    task_counter += 1
                    continue

                # Resolved unique owner
                resolved_member = matching_members[0]
                
                # Rule C: Due Date Extraction (TC1 Rule)
                due_date_str = None
                date_match = re.search(r"\bby\s+([A-Za-z0-9\-,\s]+?)(?:\.|$|,)", action_content, re.IGNORECASE)
                if date_match:
                    due_date_str = date_match.group(1).strip()
                else:
                    due_date_str = "This Week"

                confirmed_tasks.append({
                    "id": f"{transcript_id}-TASK-{task_counter}",
                    "title": action_content,
                    "owner": resolved_member["name"],
                    "owner_role": resolved_member.get("role", "Engineer"),
                    "owner_email": resolved_member.get("email", ""),
                    "due_date": due_date_str,
                    "quote": line_clean,
                    "target_board": "My Trello board",
                    "target_list": "This Week",
                    "status": "AWAITING_HUMAN_APPROVAL"
                })
                task_counter += 1

        return {
            "status": "ANALYSIS_COMPLETE",
            "transcript_id": transcript_id,
            "created_tasks": confirmed_tasks,
            "unresolved_items": tentative_items,
            "clarifications_needed": clarifications_needed,
            "evidence": f"Analyzed {len(lines)} transcript line(s). Found {len(confirmed_tasks)} confirmed task(s), {len(tentative_items)} tentative item(s), and {len(clarifications_needed)} ambiguity clarification(s)."
        }

    def execute_approved_task(self, task: Dict[str, Any], transcript_url: str = "") -> Dict[str, Any]:
        """
        Step 4 & 5:
        4. Human Approval Executed -> Creates card in Trello
        5. Verification -> Re-reads card from Trello to verify owner, date, and transcript reference
        """
        title = f"[{task['owner']}] {task['title']}"
        desc = f"""### 📋 Task Details
- **Owner:** {task['owner']} ({task.get('owner_role', 'Team Member')})
- **Due:** {task.get('due_date', 'Not specified')}

---
### 🎙️ Source Evidence & Transcript Quote
> "{task['quote']}"

- **Source Reference:** {transcript_url or 'Meeting Transcript ID: ' + task['id']}
- **Created By:** Meeting-to-Tasks AI Agent (Agentic Hackathon 2026)
"""
        # Calculate standard due date string for Trello (e.g. 5 days from today)
        due_iso = (datetime.datetime.now() + datetime.timedelta(days=5)).isoformat()

        # Step 4: Create Card on Trello
        created_card = self.trello.create_card(
            title=title,
            description=desc,
            due_date=due_iso,
            list_id=TRELLO_DEFAULT_LIST_ID
        )

        card_id = created_card["id"]
        card_url = created_card["shortUrl"]

        # Step 5: Independent Verification Rule
        verification = self.trello.verify_card(
            card_id=card_id,
            expected_owner=task["owner"],
            expected_date=due_iso[:10],
            expected_transcript_ref=task["quote"]
        )

        # Store in DB
        with self._get_connection() as conn:
            conn.execute(
                """INSERT OR REPLACE INTO tasks 
                   (id, transcript_id, title, owner, due_date, quote, status, trello_card_id, trello_url, verified) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (task["id"], task.get("transcript_id", "T1"), task["title"], task["owner"], 
                 task.get("due_date", ""), task["quote"], "EXECUTED", card_id, card_url, 1 if verification["verified"] else 0)
            )
            conn.commit()

        return {
            "success": True,
            "trello_card_id": card_id,
            "trello_card_url": card_url,
            "verification": verification
        }
