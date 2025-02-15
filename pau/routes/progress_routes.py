import os
import json
import matplotlib.pyplot as plt
import numpy as np
from flask import Blueprint, jsonify, url_for, send_file
import datetime

progress_bp = Blueprint("progress", __name__)

# Define paths
SCORES_FILE = os.path.join("data", "scores.json")
GRAPH_DIR = "generated_graphs"
PROGRESS_GRAPH = os.path.join(GRAPH_DIR, "progress_graph.png")

if not os.path.exists(GRAPH_DIR):
    os.makedirs(GRAPH_DIR, exist_ok=True)
    print(f"✅ Created directory: {GRAPH_DIR}")


MODULE_COLORS = {
    "python": "blue",
    "aws": "green",
    "devops": "orange",
    "networking": "red"
}

def load_scores():
    """Load scores from scores.json."""
    if not os.path.exists(SCORES_FILE):
        print("⚠️ scores.json not found.")
        return {}
    
    with open(SCORES_FILE, "r") as file:
        return json.load(file)

def extract_progress(data):
    """Extract dates and scores for all modules."""
    scores = {}
    for module, records in data.items():
        module_scores = []
        module_dates = []
        for entry in records:
            if "score" in entry and "date" in entry:
                try:
                    # Convert timestamp string to datetime object
                    date_obj = datetime.datetime.strptime(entry["date"], "%Y-%m-%d %H:%M:%S")
                    module_scores.append(entry["score"])
                    module_dates.append(date_obj.strftime("%b %d %H:%M"))  # Format date (e.g., "Feb 15 21:30")
                except ValueError:
                    continue  # Skip invalid dates

        if module_scores:
            scores[module] = {"dates": module_dates, "scores": module_scores}
    
    return scores

def plot_progress(scores):
    """Generate a bar chart for progress and save it in 'generated_graphs/'."""
    if not scores:
        print("⚠️ No valid scores data found. Skipping graph generation.")
        return  

    print(f"📊 Generating graph for scores: {scores}")

    plt.figure(figsize=(10, 6))

    # Get all unique dates across modules
    all_dates = sorted(set(date for module in scores.values() for date in module["dates"]))
    index = np.arange(len(all_dates))  # Generate X positions

    bar_width = 0.2  # Width for bars

    for i, (module, data) in enumerate(scores.items()):
        # Map module-specific dates to global index positions
        y_values = [data["scores"][data["dates"].index(date)] if date in data["dates"] else 0 for date in all_dates]

        plt.bar(index + (i * bar_width), y_values, bar_width, label=module.capitalize())

    plt.xlabel("Date")
    plt.ylabel("Score")
    plt.title("Quiz Progress Over Time")
    plt.xticks(index + bar_width / 2, all_dates, rotation=45)
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    # Save the graph in the new directory
    try:
        plt.savefig(PROGRESS_GRAPH, dpi=150)
        print(f"✅ Progress graph successfully saved: {PROGRESS_GRAPH}")
    except Exception as e:
        print(f"❌ Error saving progress graph: {e}")

    plt.close()

    
@progress_bp.route("/progress/graph")
def get_progress_graph():
    """Serve the progress graph from the 'generated_graphs/' directory."""
    graph_path = os.path.abspath(os.path.join("generated_graphs", "progress_graph.png"))

    if not os.path.exists(graph_path):
        print("❌ Error: Graph file not found in 'generated_graphs/' folder!")
        return jsonify({"error": "Graph not found"}), 404

    return send_file(graph_path, mimetype="image/png")

@progress_bp.route("/progress/update")
def update_progress():
    """Generate and return progress graph path from 'generated_graphs/'."""
    data = load_scores()
    if not data:
        return jsonify({"error": "No progress data available."}), 400

    scores = extract_progress(data)
    plot_progress(scores)

    return jsonify({"progressGraph": "/progress/graph"})  # Serve from new directory