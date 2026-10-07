import os
import mimetypes
from pathlib import Path
from core.config import UPLOAD_DIR
from core.gemini_client import upload_file_to_gemini

# Register common video/audio/pdf MIME types
mimetypes.add_type("video/mp4", ".mp4")
mimetypes.add_type("audio/mpeg", ".mp3")
mimetypes.add_type("audio/wav", ".wav")
mimetypes.add_type("application/pdf", ".pdf")

from pypdf import PdfReader

class MultimodalDocumentBundle:
    def __init__(self):
        self.files = []  # List of dicts with name, local_path, mime_type, gemini_file, text_content
        self.metadata = {
            "title": "",
            "topics_detected": [],
            "duration_seconds": 0,
            "page_count": 0
        }

    def add_file(self, file_path: str | Path, custom_name: str = None, use_gemini_api: bool = True, *args, **kwargs):
        path_obj = Path(file_path)
        mime_type, _ = mimetypes.guess_type(str(path_obj))
        if not mime_type:
            if path_obj.suffix.lower() == ".pdf":
                mime_type = "application/pdf"
            elif path_obj.suffix.lower() in [".mp4", ".mov", ".avi", ".mkv"]:
                mime_type = "video/mp4"
            elif path_obj.suffix.lower() in [".mp3", ".wav", ".m4a"]:
                mime_type = "audio/mpeg"
            else:
                mime_type = "text/plain"

        gemini_file = None
        extracted_text = ""

        # Local PDF extraction
        if mime_type == "application/pdf":
            try:
                reader = PdfReader(str(path_obj))
                extracted_text = "\n".join([page.extract_text() or "" for page in reader.pages])
                self.metadata["page_count"] += len(reader.pages)
            except Exception as e:
                print(f"Local PDF read warning: {e}")

        # Upload to Gemini File API if enabled
        if use_gemini_api:
            try:
                gemini_file = upload_file_to_gemini(path_obj, mime_type=mime_type)
            except Exception as e:
                print(f"Gemini API upload fallback: {e}")

        file_entry = {
            "name": custom_name or path_obj.name,
            "local_path": str(path_obj),
            "mime_type": mime_type,
            "gemini_file": gemini_file,
            "text_content": extracted_text
        }
        self.files.append(file_entry)
        return file_entry

    def get_gemini_file_handles(self):
        """Returns the list of uploaded Gemini file objects ready to pass to the model."""
        return [f["gemini_file"] for f in self.files if f.get("gemini_file") is not None]

    def get_all_text(self):
        """Returns aggregated text content from all local ingested files."""
        return "\n\n".join([f["text_content"] for f in self.files if f.get("text_content")])

def save_uploaded_file(uploaded_file, save_directory: Path = UPLOAD_DIR) -> Path:
    """Saves a Streamlit UploadedFile to disk."""
    save_path = save_directory / uploaded_file.name
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return save_path

