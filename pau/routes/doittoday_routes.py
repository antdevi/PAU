import os
import json
import re
import time
import datetime
from flask import Blueprint, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("❌ OpenAI API Key is missing. Check your .env file!")

# ✅ Initialize OpenAI Client
client = OpenAI(api_key=openai_api_key)

# Define Blueprint
doittoday_bp = Blueprint('doittoday', __name__)

# File paths
NOTES_FILE = "data/notes/notes.json"
CHAT_HISTORY_FILE = "log/chat_history.json"
USER_SCORES_FILE = "data/doittoday_scores.json"

def load_json_file(file_path):
    """
    Load and return the content of a JSON file.
    
    :param file_path: Path to the JSON file.
    :return: Parsed content of the file.
    """

    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}. Returning empty list.")
        return []
    
def get_today_date():
    """Return today's date in YYYY-MM-DD format."""
    return datetime.datetime.now().strftime("%Y-%m-%d")


def extract_today_topics():
    """Extract topics from today's notes and chat history."""
    today = get_today_date()
    
    # Load Notes
    notes_data = load_json_file(NOTES_FILE)
    today_topics = set()

    for note in notes_data:
        if "date" in note and note["date"].startswith(today):
            if "title" in note:
                today_topics.add(note["title"])
            if "content" in note:
                today_topics.update(note["content"].split("\n"))

    # Load Chat History
    chat_data = load_json_file(CHAT_HISTORY_FILE)
    today_chats = set()

    for chat in chat_data:
        if "timestamp" in chat and chat["timestamp"].startswith(today):
            if "message" in chat:
                today_chats.update(chat["message"].split())

    # Combine both sources
    combined_topics = today_topics.union(today_chats)
    return list(combined_topics) if combined_topics else ["General Knowledge"]

def generate_quiz(quiz_topics, num_questions=15, max_retries=3):
    """Generate multiple-choice quiz questions based on topics and chat history."""
    for attempt in range(max_retries):
        try:
            prompt = f"""
            Generate {num_questions} multiple-choice questions based on these topics:
            {", ".join(quiz_topics)}

            Each question should:
            - Have 4 answer choices (A, B, C, D)
            - Specify the correct answer
            - Follow this JSON format:
            [
                {{"question": "What is AWS?", "options": ["A. Cloud Service", "B. Database", "C. Storage Device", "D. Network"], "correct_answer": "A"}}
            ]
            """

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an AI that generates multiple-choice questions based on recent notes and chat history."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                timeout=60
            )

            quiz_content = response.choices[0].message.content.strip()
            print("🟢 Raw OpenAI response:", quiz_content)  # Debugging

            # Ensure JSON-like response
            if not quiz_content.startswith("[") or not quiz_content.endswith("]"):
                print("⚠️ OpenAI returned invalid JSON. Retrying...")
                continue

            quiz = json.loads(quiz_content)  # Parse JSON response
            if isinstance(quiz, list) and all("question" in q and "options" in q and "correct_answer" in q for q in quiz):
                return quiz
            else:
                print("Invalid JSON structure from OpenAI:", quiz_content)
                continue  # Retry if format is incorrect

        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}. Raw response:", quiz_content)
            continue  # Retry if parsing fails
        except Exception as e:
            print(f"Error generating quiz: {e}. Retrying in 5 seconds...")
            time.sleep(5)

    print("⚠️ OpenAI failed to generate valid questions after retries.")
    return [{"question": "Error occurred", "options": ["A", "B", "C", "D"], "correct_answer": "A"}]  # Prevent crashes

def load_user_scores():
    """Load user quiz scores from a JSON file."""
    if not os.path.exists(USER_SCORES_FILE):
        return []
    
    with open(USER_SCORES_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_user_scores(data):
    """Save quiz results to a JSON file."""
    with open(USER_SCORES_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

@doittoday_bp.route('/generate_quiz', methods=['GET'])
def get_quiz():
    """API to generate and return a quiz."""
    topics = extract_today_topics()
    quiz_questions = generate_quiz(topics, num_questions=20)
    return jsonify({"quiz": quiz_questions})

@doittoday_bp.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    """API to handle quiz submission and calculate the score."""
    data = request.json
    user_answers = data.get("answers", {})
    quiz = data.get("quiz", [])
    if not quiz:
        return jsonify({"error": "No quiz data provided"}), 400
    score = 0
    quiz_results = []
    for question_data in quiz:

        question_text = question_data["question"]
        correct_answer = question_data["correct_answer"]
        user_answer = user_answers.get(question_data["question"], None)

        is_correct = user_answer == correct_answer
        if is_correct:
            score += 1
        
        quiz_results.append({
            "question": question_text,
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "correct": is_correct
        })

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Load existing scores
    user_scores = load_user_scores()

    # Append new results
    user_scores.append({
        "date": timestamp,
        "score": score,
        "total_questions": len(quiz),
        "results": quiz_results
    })

    # Save updated scores
    save_user_scores(user_scores)

    return jsonify({
        "score": f"{score}/{len(quiz)}",
        "date": timestamp,
        "results": quiz_results
    })
