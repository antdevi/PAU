import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    LOG_DIR = os.path.join(BASE_DIR, "../log")  # Store logs in the log/ folder
    CHAT_HISTORY_FILE = os.path.join(LOG_DIR, "chat_history.json")
    
    # OpenAI API Key (Read from Environment Variables)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")