from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import openai
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

# Flask application setup
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Secret key for session management

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Define ChatLog model
class ChatLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_input = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Define AnswerLog model (for saving quiz answers)
class AnswerLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    question = db.Column(db.String(500), nullable=False)
    selected_option = db.Column(db.String(100), nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    is_correct = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# OpenAI API setup
openai.api_key = 'your-api-key-here'

# Route: Login Page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            session['answered_questions'] = []  # Initialize answered questions list
            return redirect(url_for('chat'))
        else:
            return render_template('login.html', error="Invalid username or password.")

    return render_template('login.html')

# Route: Forgot Password Page
@app.route('/forgetpassword', methods=['GET', 'POST'])
def forget_password():
    return render_template('forgetpassword.html')

# Route: Serve Chat Page
@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("chat.html", username=session['username'])

# New API Route: Get a Random Question
@app.route('/get_question', methods=['GET'])
def get_question():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    # Initialize answered questions in session if not already present
    if 'answered_questions' not in session:
        session['answered_questions'] = []
    
    # Load questions from JSON file
    try:
        with open('static/python_quiz_questions.json', 'r') as f:
            all_questions = json.load(f)
    except Exception as e:
        return jsonify({"error": "Failed to load questions."}), 500

    # Filter out answered questions
    unanswered_questions = [q for q in all_questions if q['question'] not in session['answered_questions']]

    if not unanswered_questions:
        return jsonify({"message": "No unanswered questions remaining!"}), 200

    # Select a random question from the unanswered pool
    question_data = unanswered_questions[0]  # You can randomize further if needed

    return jsonify({
        "question": question_data['question'],
        "options": question_data['options']
    })

# API Route to save the answer
@app.route('/save_answer', methods=['POST'])
def save_answer():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    
    try:
        question = data['question']
        selected_option = data['selectedOption']
        is_correct = data['isCorrect']
        explanation = data['explanation']

        # Save the answer to the database
        save_answer_to_db(session['username'], question, selected_option, explanation, is_correct)

        # Mark the question as answered
        if question not in session['answered_questions']:
            session['answered_questions'].append(question)

        return jsonify({"message": "Answer saved successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Function to save answers to the database
def save_answer_to_db(user_name, question, selected_option, explanation, is_correct):
    answer = AnswerLog(
        user_name=user_name,
        question=question,
        selected_option=selected_option,
        explanation=explanation,
        is_correct=is_correct
    )
    db.session.add(answer)
    db.session.commit()

# Route: View Logs
@app.route("/logs")
def view_logs():
    if 'username' not in session:
        return redirect(url_for('login'))

    logs = ChatLog.query.order_by(ChatLog.timestamp.desc()).all()
    return render_template("logs.html", logs=logs)

# Route: Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('answered_questions', None)  # Clear answered questions session
    return redirect(url_for('login'))

if __name__ == "__main__":
    # Create database tables within the application context
    with app.app_context():
        db.create_all()
        # Create a default user for login
        if not User.query.filter_by(username="admin").first():
            db.session.add(User(username="admin", password="password"))
            db.session.commit()
    app.run(debug=True)
