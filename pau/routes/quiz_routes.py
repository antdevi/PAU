import os
import json
import random
import datetime
from flask import Blueprint, request, jsonify, render_template

quiz_bp = Blueprint("quiz", __name__)

# Define file paths for questions and scores
QUESTIONS_FILE = "data/question_quiz.json"
SCORE_FILE = "data/scores.json"

def load_questions():
    """Load questions from the JSON file."""
    if not os.path.exists(QUESTIONS_FILE):
        return {}
    with open(QUESTIONS_FILE, "r") as file:
        return json.load(file)

def load_scores():
    """Load scores from the JSON file."""
    if not os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "w") as file:
            json.dump({}, file)
    with open(SCORE_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}

def save_scores(data):
    """Save scores to the JSON file."""
    with open(SCORE_FILE, "w") as file:
        json.dump(data, file, indent=4)

# 🟢 Route to Render the Quiz Page
@quiz_bp.route("/quiz/<module_name>")
def quiz_page(module_name):
    """Render the quiz page for the selected module."""
    all_questions = load_questions()
    if module_name not in all_questions:
        return jsonify({"error": "Module not found"}), 404
    # The quiz.html template will use JavaScript to fetch questions via API
    return render_template("quiz.html", module=module_name)

# 🔵 API to Fetch Quiz Questions
@quiz_bp.route("/api/quiz/<module_name>", methods=["GET"])
def get_quiz(module_name):
    """Fetch a set of random questions for the selected module."""
    all_questions = load_questions()
    if module_name not in all_questions:
        return jsonify({"error": "Module not found"}), 404
    selected_questions = random.sample(all_questions[module_name], min(5, len(all_questions[module_name])))
    return jsonify(selected_questions)

# 🟡 API to Submit Answers and Calculate Score
@quiz_bp.route("/api/submit_quiz", methods=["POST"])
def submit_quiz():
    """
    Process the quiz submission.
    Expects a JSON with:
      - module: The module name (e.g., "python")
      - answers: A list of answer objects. Each object should include:
          question, user_answer, correct_answer, correct, subjective.
    """
    data = request.get_json()
    module = data.get("module")
    answers = data.get("answers")

    if not module or not answers:
        return jsonify({"error": "Invalid submission data"}), 400
    
    # Calculate the score
    score = sum(10 if answer.get("correct") else -5 for answer in answers)

    # Get current timestamp (YYYY-MM-DD HH:MM:SS format)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    # Load existing scores
    scores = load_scores()
    if module not in scores:
        scores[module] = []

    # Append new score with timestamp
    scores[module].append({
        "score": score,
        "date": timestamp,  # Save timestamp
        "results": answers
    })

    # Save updated scores
    save_scores(scores)

    return jsonify({"score": score, "date": timestamp, "results": answers})