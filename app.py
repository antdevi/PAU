from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from openai import OpenAI
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

# Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Secret key for session management

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Define the ChatLog model
class ChatLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_input = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Chatbot client setup
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# System instruction for the chatbot
system_instruction = {"role": "system", "content": "Always answer as a Mentor."}

# Route: Login Page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
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

# New API Route: Handle Chat Requests Asynchronously
@app.route('/get_response', methods=['POST'])
def get_response():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"error": "Message cannot be empty."}), 400

    # Chatbot API interaction
    try:
        completion = client.chat.completions.create(
            model="model-identifier",
            messages=[
                system_instruction,
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
        )
        bot_response = completion.choices[0].message.content

        # Save chat log
        save_chat_log(session['username'], user_input, bot_response)

        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route: Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Function to save chat logs to the database
def save_chat_log(user, user_input, bot_response):
    log = ChatLog(user_name=user, user_input=user_input, bot_response=bot_response)
    db.session.add(log)
    db.session.commit()

# Route: View Logs
@app.route("/logs")
def view_logs():
    if 'username' not in session:
        return redirect(url_for('login'))

    logs = ChatLog.query.order_by(ChatLog.timestamp.desc()).all()
    return render_template("logs.html", logs=logs)

if __name__ == "__main__":
    # Create database tables within the application context
    with app.app_context():
        db.create_all()
        # Create a default user for login
        if not User.query.filter_by(username="admin").first():
            db.session.add(User(username="admin", password="password"))
            db.session.commit()
    app.run(debug=True)
