import webbrowser
import time
import threading
import uvicorn
from server import app

def open_browser():
    time.sleep(1.5)
    print("\n🌐 Opening browser at http://127.0.0.1:8000 ...")
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    # Open browser automatically in background thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    print("=" * 60)
    print("🎓 Starting OmniTutor AI (Team CODEFORGE)")
    print("🌐 Server URL: http://127.0.0.1:8000 or http://localhost:8000")
    print("=" * 60)
    
    # Run uvicorn on localhost/127.0.0.1
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
