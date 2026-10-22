import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Trello Credentials
TRELLO_API_KEY = os.getenv("TRELLO_API_KEY", "b1a89de725355e9975785679121a0384")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN", "ATTA22b6b33d7268eee86d80c99d55671a3024d59129634d1a89fb70ea3deaa518edFF5E476A")
TRELLO_BOARD_ID = os.getenv("TRELLO_BOARD_ID", "6ad4e6a1950051dcf4dfb833")

# Target list on Trello for task creation (default to 'This Week' or 'Today')
TRELLO_DEFAULT_LIST_ID = os.getenv("TRELLO_DEFAULT_LIST_ID", "6ad4e6a2950051dcf4dfb83b")  # This Week list

# Gemini API Key (optional for cloud LLM parsing)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

DB_PATH = BASE_DIR / "agent_tasks.db"
