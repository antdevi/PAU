import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    LOG_DIR = os.path.join(BASE_DIR, "../log")  # Store logs in the log/ folder
    CHAT_HISTORY_FILE = os.path.join(LOG_DIR, "chat_history.json")
    
    LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"  # Ensure LM Studio is running
