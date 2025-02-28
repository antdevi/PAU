# pau/routes.py
import os
import json
import requests
from flask import Blueprint, request, jsonify
from pau.config import Config

chat_bp = Blueprint("chat", __name__)

def load_history():
    """Load the chat history from the JSON file specified in Config."""
    if os.path.exists(Config.CHAT_HISTORY_FILE):
        with open(Config.CHAT_HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    """Save the updated chat history to the JSON file."""
    os.makedirs(Config.LOG_DIR, exist_ok=True)
    with open(Config.CHAT_HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def build_messages(history):
    """
    Convert the stored history into a list of messages in the format
    expected by LM Studio.
    """
    return [{"role": item.get("role", "user"), "content": item.get("message", "")} for item in history]

def query_openai(history):
    """
    Send the full conversation history as context to OpenAI’s API.
    """
    openai_api_key = Config.OPENAI_API_KEY  # Securely read API key
    if not openai_api_key:
        return "Error: OpenAI API key is missing."
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}",
        }
    
    messages = build_messages(history)
    payload = {
        "model": "gpt-4o-mini",
        "messages": messages
    }
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        if response.ok:
            data = response.json()
            # Assuming a response format: { "choices": [ { "message": { "content": "..." } } ] }
            return data["choices"][0]["message"]["content"]
        else:
            return f"API Error: {response.status_code} - {response.text}"
    except Exception as e:
        print("Exception:", e)
        return "Sorry, an exception occurred."

@chat_bp.route("/chat", methods=["POST"])
def chat():
    """
    Chat route that receives a JSON payload with a "message" key.
    It updates the chat history, queries LM Studio with the full context,
    and returns the bot’s response.
    """
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' parameter in JSON payload"}), 400

    user_message = data["message"]

    # Load existing chat history
    history = load_history()

    # Append the user's new message
    history.append({"role": "user", "message": user_message})

    # Get bot response using LM Studio with the updated context
    bot_response = query_openai(history)

    # Append the bot's response (role 'assistant') to the history
    history.append({"role": "assistant", "message": bot_response})

    # Save the updated chat history
    save_history(history)

    return jsonify({"response": bot_response})
