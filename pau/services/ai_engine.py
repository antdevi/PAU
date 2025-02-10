import requests
from pau.config import Config

def generate_chat_response(messages):
    """Send messages to LM Studio running LLaMA 3.2 1B"""
    payload = {
        "model": "llama-3.2-1B",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 100
    }
    try:
        response = requests.post(Config.LM_STUDIO_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to connect to LM Studio: {str(e)}"}