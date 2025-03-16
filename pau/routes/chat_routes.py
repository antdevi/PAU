# pau/routes.py
import os
import json
import requests
from flask import Blueprint, request, jsonify, session, redirect, url_for, flash, render_template

from pau.config import Config
from datetime import datetime


chat_bp = Blueprint("chat", __name__, template_folder="templates")
NOTES_API_URL = "http://127.0.0.1:5000/notes/get"

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

def get_relevant_notes(user_input):
    """Fetch notes from API and find relevant topics based on user input."""
    try:
        response = requests.get(NOTES_API_URL)
        if response.status_code != 200:
            return []
        all_notes = response.json()
    except Exception as e:
        print("Error fetching notes:", e)
        return []

    relevant_notes = []
    keywords = set(user_input.lower().split())

    for note in all_notes:
        note_content = note.get("content", "").lower()
        if any(keyword in note_content for keyword in keywords):
            relevant_notes.append(note)

    return relevant_notes[:3]  # Limit to top 3 notes

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
        if response.ok:
            data = response.json()
            # Assuming a response format: { "choices": [ { "message": { "content": "..." } } ] }
            return data["choices"][0]["message"]["content"]
        else:
            return f"API Error: {response.status_code} - {response.text}"
    except Exception as e:
        print("Exception:", e)
        return "Sorry, an exception occurred."

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
