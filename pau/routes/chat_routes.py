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

def query_lm_studio(history):
    """
    Send the full conversation history as context to LM Studio.
    This example assumes that LM Studio’s API is similar to the OpenAI Chat API.
    """
    headers = {"Content-Type": "application/json"}
    messages = build_messages(history)
    payload = {
        "model": "llama-3.2-1B",
        "messages": messages
    }
    try:
        response = requests.post(Config.LM_STUDIO_URL, headers=headers, json=payload)
        if response.ok:
            data = response.json()
            # Assuming a response format: { "choices": [ { "message": { "content": "..." } } ] }
            return data["choices"][0]["message"]["content"]
        else:
            return "Sorry, an error occurred while processing your request."
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
    bot_response = query_lm_studio(history)

    # Append the bot's response (role 'assistant') to the history
    history.append({"role": "assistant", "message": bot_response})

    # Save the updated chat history
    save_history(history)

    return jsonify({"response": bot_response})
