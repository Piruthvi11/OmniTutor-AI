import os
import time
from pathlib import Path
import google.generativeai as genai
from core.config import GEMINI_API_KEY, DEFAULT_MODEL, PRO_MODEL

def configure_gemini(api_key: str = None):
    """Configures the Gemini API client with the given or environment API key."""
    key = api_key or GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
    if not key:
        return False
    genai.configure(api_key=key)
    return True

def upload_file_to_gemini(file_path: str | Path, mime_type: str = None):
    """
    Uploads video, audio, or PDF files to Google Gemini File API.
    Waits for processing to complete if it's a video file.
    """
    path_obj = Path(file_path)
    if not path_obj.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Upload using File API
    uploaded_file = genai.upload_file(path=str(path_obj), mime_type=mime_type)
    
    # If video or audio, poll until ACTIVE state is reached
    while uploaded_file.state.name == "PROCESSING":
        time.sleep(2)
        uploaded_file = genai.get_file(uploaded_file.name)

    if uploaded_file.state.name == "FAILED":
        raise ValueError(f"File processing failed on Gemini: {uploaded_file.error.message}")

    return uploaded_file

FALLBACK_MODELS = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro",
    "gemini-1.5-pro-latest",
    "gemini-2.0-flash",
    "gemini-pro"
]

def get_gemini_model(model_name: str = DEFAULT_MODEL, system_instruction: str = None):
    """Instantiates a GenerativeModel with optional system instructions and model fallback."""
    generation_config = {
        "temperature": 0.3,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 4096,
    }
    
    models_to_try = [model_name] + [m for m in FALLBACK_MODELS if m != model_name]
    last_err = None
    
    for candidate in models_to_try:
        try:
            return genai.GenerativeModel(
                model_name=candidate,
                generation_config=generation_config,
                system_instruction=system_instruction
            )
        except Exception as e:
            last_err = e
            continue
            
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=system_instruction
    )
