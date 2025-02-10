import json
import os
from pau.config import Config

def ensure_log_directory():
    """Ensure the log directory exists before saving files."""
    if not os.path.exists(Config.LOG_DIR):
        os.makedirs(Config.LOG_DIR)

def load_json(filepath, default_value=None):
    """Load a JSON file safely."""
    ensure_log_directory()  # Ensure the log directory exists
    if not os.path.exists(filepath):
        return default_value or []
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def save_json(filepath, data):
    """Save data to a JSON file safely."""
    ensure_log_directory()  # Ensure the log directory exists
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
