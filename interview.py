from flask import Flask, render_template, jsonify, request
import random
import json
from datetime import datetime
import os

app = Flask(__name__)

data_folder = 'quiz'  
file_path = os.path.join(data_folder, 'scores.json')

if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Load questions from a JSON file
def load_questions():
    with open('python_quiz.json', 'r') as file:
        questions = json.load(file)
    return questions

# Store answers and scores with timestamp
def store_score(answer_data):
    # Get the current date and time for the timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    answer_data['timestamp'] = timestamp
    
    # Save the score data to scores.json file
    with open('scores.json', 'a') as file:
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
    
    # Log the received data for debugging
    print("Received Data: ", data)
    
    # Store the score along with the timestamp
    store_score(data)
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
