from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import openai
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
import traceback
import subprocess
import os 

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

quiz_process = subprocess.Popen(["python", "quiz.py"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
@app.route("/quiz")
def quiz_redirect():
    return "Redirecting to Quiz App", 302, {"Location": "http://127.0.0.1:5001/"}

if __name__ == "__main__":
    try:
        print("Starting PAU App...")
        app.run(debug=True, port=5000)  # Run PAU on port 5000
    finally:
        print("Stopping Quiz App...")
        quiz_process.terminate()
        

if __name__ == "__main__":
    # Create database tables within the application context
    with app.app_context():
        db.create_all()
        # Create a default user for login
        if not User.query.filter_by(username="admin").first():
            db.session.add(User(username="admin", password="password"))
            db.session.commit()
    app.run(debug=True)