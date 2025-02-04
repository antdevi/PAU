from flask import Flask, render_template, jsonify, request
import random
import json
from datetime import datetime
import os
app = Flask(__name__)

# Define the folder where you want to store the JSON file (e.g., "data" folder)
data_folder = 'data'  # You can change this to any folder you prefer
file_path = os.path.join(data_folder, 'scores.json')  # Path to the JSON file

# Make sure the directory exists, otherwise create it
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Load questions from a JSON file
def load_questions():
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'python_quiz.json')

    with open(file_path, 'r') as file:
        questions = json.load(file)
    return questions

# Store answers and scores with timestamp
def store_score(answer_data):
    # Get the current date and time for the timestamp (if needed in backend)
    timestamp = answer_data.get('timestamp', None)
    
    # Save the score data to scores.json file in the desired folder
    with open(file_path, 'a') as file:
        json.dump(answer_data, file)
        file.write('\n')  # Separate entries with new lines

@app.route('/')
def index():
    return render_template('quiz.html')

@app.route('/get_question', methods=['GET'])
def get_random_question():
    questions = load_questions()
    question = random.choice(questions)  # Get a random question
    return jsonify(question)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.json
    store_score(data)  # Store the user's answer and score along with timestamp
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5001)
