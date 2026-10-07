import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
SAMPLE_DIR = BASE_DIR / "data" / "sample_materials"

# Ensure directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Default Models
DEFAULT_MODEL = "gemini-1.5-flash"  # Fast, highly accurate multimodal understanding
PRO_MODEL = "gemini-1.5-pro"        # Deep reasoning model for complex academic papers
