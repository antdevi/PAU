import os
import json
from flask import Blueprint, request, jsonify
from datetime import datetime

notes_bp = Blueprint("notes", __name__)

NOTES_DIR = "data/notes"
NOTES_FILE = os.path.join(NOTES_DIR, "notes.json")

# Ensure directory exists
if not os.path.exists(NOTES_DIR):
    os.makedirs(NOTES_DIR)

# Ensure file exists
if not os.path.exists(NOTES_FILE):
    with open(NOTES_FILE, "w") as f:
        json.dump([], f)


# Route to save a note
@notes_bp.route("/save", methods=["POST"])
def save_note():
    data = request.json
    note = {
        "id": data.get("id"),
        "title": data.get("title"),
        "content": data.get("content"),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(NOTES_FILE, "r+") as f:
        notes = json.load(f)
        notes.append(note)
        f.seek(0)
        json.dump(notes, f, indent=4)

    return jsonify({"success": True})


# Route to get all notes
@notes_bp.route("/get", methods=["GET"])
def get_notes():
    with open(NOTES_FILE, "r") as f:
        notes = json.load(f)
    return jsonify(notes)


# Route to delete selected notes
@notes_bp.route("/delete", methods=["POST"])
def delete_notes():
    data = request.json
    ids_to_delete = set(data.get("ids", []))

    with open(NOTES_FILE, "r+") as f:
        notes = json.load(f)
        notes = [note for note in notes if str(note["id"]) not in ids_to_delete]
        f.seek(0)
        f.truncate()
        json.dump(notes, f, indent=4)

    return jsonify({"success": True})


# Route to open selected notes
@notes_bp.route("/open", methods=["POST"])
def open_notes():
    data = request.json
    ids_to_open = set(map(str, data.get("ids", [])))  # Convert IDs to string

    with open(NOTES_FILE, "r") as f:
        notes = json.load(f)
        selected_notes = [note for note in notes if str(note["id"]) in ids_to_open]

    return jsonify(selected_notes)