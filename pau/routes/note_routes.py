import os
import json
from flask import Blueprint, request, jsonify, session
from datetime import datetime

notes_bp = Blueprint("notes", __name__)

NOTES_DIR = "data/notes"
os.makedirs(NOTES_DIR, exist_ok=True)  # Ensure the notes directory exists

def get_user_notes_file():
    """Returns the file path for the logged-in user's notes."""
    username = session.get("user")
    if not username:
        return None  # No user logged in
    return os.path.join(NOTES_DIR, f"{username}_notes.json")

def load_notes():
    """Load notes from the user's specific JSON file."""
    user_file = get_user_notes_file()
    if not user_file:
        return []
    
    if not os.path.exists(user_file):
        return []  # No notes exist for this user

    try:
        with open(user_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []  # Handle corrupted JSON files

def save_notes(notes):
    """Save notes to the user's specific JSON file."""
    user_file = get_user_notes_file()
    if not user_file:
        return False

    with open(user_file, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=4)
    return True

# ✅ Route to save a note
@notes_bp.route("/save", methods=["POST"])
def save_note():
    if "user" not in session:
        return jsonify({"error": "User not logged in"}), 401

    data = request.json
    if not data or "title" not in data or "content" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    note = {
        "id": data.get("id", datetime.now().timestamp()),  # Generate unique ID if missing
        "title": data["title"],
        "content": data["content"],
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    notes = load_notes()
    notes.append(note)

    if save_notes(notes):
        print(f"✅ Note Saved: {note}")  # ✅ Debugging: Check if notes are being saved
        return jsonify({"success": True, "note": note})
    
    return jsonify({"error": "Failed to save note"}), 500

# ✅ Route to get all notes
@notes_bp.route("/get", methods=["GET"])
def get_notes():
    if "user" not in session:
        return jsonify({"error": "User not logged in"}), 401

    keyword = request.args.get("keyword", "").strip().lower()  # Get keyword from query params
    notes = load_notes()

    print(f"📌 Stored Notes: {notes}")  # ✅ Debugging

    if keyword:
        filtered_notes = [
            note for note in notes if keyword in note.get("content", "").strip().lower() or 
                                     keyword in note.get("title", "").strip().lower()
        ]
        print(f"🔍 Filtered Notes for '{keyword}': {filtered_notes}")  # ✅ Debugging
        return jsonify(filtered_notes)

    return jsonify(notes)

# ✅ Route to delete selected notes
@notes_bp.route("/delete", methods=["POST"])
def delete_notes():
    if "user" not in session:
        return jsonify({"error": "User not logged in"}), 401

    data = request.json
    ids_to_delete = set(map(str, data.get("ids", [])))

    notes = [note for note in load_notes() if str(note["id"]) not in ids_to_delete]
    
    if save_notes(notes):
        print(f"🗑️ Deleted Notes: {ids_to_delete}")  # ✅ Debugging
        return jsonify({"success": True})
    
    return jsonify({"error": "Failed to delete notes"}), 500

# ✅ Route to open selected notes
@notes_bp.route("/open", methods=["POST"])
def open_notes():
    if "user" not in session:
        return jsonify({"error": "User not logged in"}), 401

    data = request.json
    ids_to_open = set(map(str, data.get("ids", [])))

    selected_notes = [note for note in load_notes() if str(note["id"]) in ids_to_open]

    print(f"📖 Opened Notes: {selected_notes}")  # ✅ Debugging
    return jsonify(selected_notes)
