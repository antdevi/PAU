# pau/routes.py
import os
import json
import requests
from flask import Blueprint, request, jsonify, session, redirect, url_for, flash, render_template

from pau.config import Config
from datetime import datetime


chat_bp = Blueprint("chat", __name__, template_folder="templates")
NOTES_API_URL = "http://127.0.0.1:5000/notes/get"

def get_user_chat_file():
    """Return chat history file path for the logged-in user."""
    username = session.get("user")
    if not username:
        return None  # No user logged in
    return os.path.join(Config.LOG_DIR, f"{username}_chat.json")

def load_history():
    """Load user-specific chat history from JSON."""
    chat_file = get_user_chat_file()
    if not chat_file:
        return []
    
    if not os.path.exists(chat_file):
        return []  # No chat history yet

    try:
        with open(chat_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []  # Handle corrupted files

def save_history(history):
    """Save user-specific chat history."""
    chat_file = get_user_chat_file()
    if not chat_file:
        return False

    os.makedirs(Config.LOG_DIR, exist_ok=True)  # Ensure log directory exists
    with open(chat_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)
    return True

def get_relevant_notes(user_input):
    """Fetch notes from API and find relevant topics based on user input."""
    try:
        response = requests.get(f"{NOTES_API_URL}?keyword={user_input}")
        return response.json() if response.status_code == 200 else []
    except Exception as e:
        print("Error fetching notes:", e)
        return []

def build_messages(history, notes):
    """
    Convert the stored history into a list of messages in the format
    expected by LM Studio.
    """
    messages = [{"role": item.get("role", "user"), "content": item.get("message", "")} for item in history]
    if notes:
        note_content = "\n".join([f"{note['title']}: {note['content']}" for note in notes])
        messages.insert(0, {"role": "system", "content": f"User notes:\n{note_content}"})

    return messages

def query_openai(history, notes):
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
    
    messages = build_messages(history, notes)
    payload = {
        "model": "gpt-4o-mini",
        "messages": messages
    }
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors (400, 500, etc.)
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"OpenAI API Error: {e}")
        return "Sorry, the assistant is currently unavailable."

@chat_bp.route("/chat", methods=["GET"])
def chat_page():
    """Serve the PAU Chat Page after login."""
    if "user" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("auth.home"))  # Redirect to login if not authenticated
    return render_template("chat.html")

@chat_bp.route("/chat", methods=["POST"])
def chat():
    """
    Chat route that receives a JSON payload with a "message" key.
    It updates the chat history, queries LM Studio with the full context,
    and returns the bot’s response.
    """
    if "user" not in session:
        return jsonify({"error": "User not logged in"}), 401  # Unauthorized
    
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' parameter in JSON payload"}), 400

    user_message = data["message"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Load existing chat history
    history = load_history()

    # Get relevant notes based on the user message
    relevant_notes = get_relevant_notes(user_message)

    # Append the user's new message
    history.append({"role": "user", "message": user_message, "timestamp": timestamp})

    # Get bot response using LM Studio with the updated context
    bot_response = query_openai(history, relevant_notes)

    # Append the bot's response (role 'assistant') to the history
    history.append({"role": "assistant", "message": bot_response, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

    # Save the updated chat history
    save_history(history)

    return jsonify({"response": bot_response, "format": "markdown"})
