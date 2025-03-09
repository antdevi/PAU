from flask import Blueprint, jsonify, request, send_from_directory, current_app
import json
import datetime
import os
import openai
import numpy as np
import matplotlib.pyplot as plt
import re
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

progress_bp = Blueprint("progress", __name__)

# Load JSON files
def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read().strip()
            if not data:
                print(f"Warning: {file_path} is empty. Returning an empty dictionary.")
                return {}
            json_data = json.loads(data)
            return json_data if isinstance(json_data, dict) else {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}. Returning an empty dictionary.")
        return {}
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Please check the file path.")
        return {}

# Analyze study progress for all modules
def analyze_study_progress(scores_data, tasks_data):
    module_progress = {}

    for module, attempts in scores_data.items():
        total_score = 0
        num_attempts = 0
        module_study_days = set()

        for attempt in attempts:
            total_score += attempt["score"]
            num_attempts += 1

            if "date" in attempt:
                module_study_days.add(attempt["date"])

        avg_score = total_score / num_attempts if num_attempts > 0 else 0
        study_days = len(module_study_days)

        module_progress[module] = {
            "avg_score": avg_score,
            "num_attempts": num_attempts,
            "study_days": study_days
        }

    return module_progress

# Predict completion time for each module using OpenAI
def predict_completion_time(module_name, avg_score, study_days):
    prompt = f"""
    Given that the student is studying {module_name}, with an average test score of {avg_score:.2f}%, 
    and has studied for {study_days} days, predict how many more days they need to master this module. 
    Assume increasing complexity as the learning progresses.
    Provide only a number representing the predicted number of days.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    prediction_text = response.choices[0].message.content
    match = re.search(r"\b\d+\b", prediction_text)

    if match:
        return int(match.group())  # Extract and return the number
    else:
        print(f"Warning: No valid number found for {module_name}. Defaulting to 30 days.")
        return 30  # Default if OpenAI fails to return a number

# Generate progress graph for all modules
def generate_progress_graph(module_name, study_days, predicted_days_needed, avg_score):
    x = np.arange(1, predicted_days_needed + 1)
    y = np.cumsum(np.random.normal(study_days / max(1, predicted_days_needed), 2, predicted_days_needed))  

    plt.figure(figsize=(10, 5))
    plt.plot(x, y, marker='o', linestyle='-', label=f"Predicted Progress for {module_name}")
    plt.axhline(y=study_days, color='r', linestyle='--', label="Current Progress")

    plt.annotate(f"Avg Score: {avg_score}%", xy=(0.5, 0.9), xycoords="axes fraction", fontsize=12, color="blue")

    plt.xlabel("Study Sessions")
    plt.ylabel("Days Taken")
    plt.title(f"{module_name} Progress Prediction")
    plt.legend()
    plt.grid(True)

    save_dir = "generated_graphs/progress_graphs"
    os.makedirs(save_dir, exist_ok=True)

    # Save the graph as an image
    image_path = os.path.join(save_dir, f"{module_name}_progress.png")
    plt.savefig(image_path)
    plt.close()  # Close plot to prevent memory leaks

    return image_path  # Return the saved image path

progress_bp.route('/progress/predict', methods=['POST'])
def predict_progress():
    data = request.json
    module_name = data.get("module_name")
    avg_score = data.get("avg_score")
    study_days = data.get("study_days")

    predicted_days_needed = predict_completion_time(module_name, avg_score, study_days)
    return jsonify({"predicted_days": predicted_days_needed})

@progress_bp.route('/progress/graph', methods=['POST'])
def get_progress_graph():
    data = request.json
    module_name = data.get("module_name")
    avg_score = data.get("avg_score")
    study_days = data.get("study_days")

    predicted_days_needed = predict_completion_time(module_name, avg_score, study_days)
    graph_path = generate_progress_graph(module_name, study_days, predicted_days_needed, avg_score)

    return jsonify({"graph_path": graph_path})

# Serve progress graphs
@progress_bp.route('/progress/graph/<filename>')
def serve_progress_graph(filename):
    directory = os.path.abspath("generated_graphs/progress_graphs")  # Absolute path
    return send_from_directory(directory, filename)

# File paths
scores_path = "data/scores.json"
tasks_path = "data/doittoday_scores.json"

# Load data
scores_data = load_json(scores_path)
tasks_data = load_json(tasks_path)

# Analyze progress
module_progress = analyze_study_progress(scores_data, tasks_data)

# Predict time needed for each module
for module, data in module_progress.items():
    predicted_days_needed = predict_completion_time(module, data["avg_score"], data["study_days"])
    print(f"Predicted Time Required for {module}: {predicted_days_needed} days")

    # Generate progress graph
    generate_progress_graph(module, data["study_days"], predicted_days_needed, data["avg_score"])