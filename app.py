from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Flask application
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

# Flask route for the chatbot interface
@app.route("/")
def index():
    return render_template("index.html")

# Function to save chat logs to the database
def save_chat_log(user, user_input, bot_response):
    log = ChatLog(user_name=user, user_input=user_input, bot_response=bot_response)
    db.session.add(log)
    db.session.commit()

# Flask route to handle chatbot interactions
@app.route("/chat", methods=["POST"])
def chat():
    user_name = request.form.get("name", "User")
    user_input = request.form.get("message", "")

    if not user_input.strip():
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

        # Save the conversation to the database
        save_chat_log(user_name, user_input, bot_response)

        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Flask route to view chat logs
@app.route("/logs")
def view_logs():
    logs = ChatLog.query.order_by(ChatLog.timestamp.desc()).all()
    return render_template("logs.html", logs=logs)

# HTML templates
INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Chatbot Interface</title>
</head>
<body>
    <h1>Chat with the Bot</h1>
    <form id="chat-form">
        <label for="name">Your Name:</label>
        <input type="text" id="name" name="name" required><br><br>
        <label for="message">Your Message:</label>
        <textarea id="message" name="message" required></textarea><br><br>
        <button type="submit">Send</button>
    </form>
    <div id="chat-response"></div>

    <script>
        document.getElementById('chat-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('name').value;
            const message = document.getElementById('message').value;

            const responseDiv = document.getElementById('chat-response');
            responseDiv.textContent = "Thinking...";

            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({ name, message })
            });

            const result = await response.json();

            if (response.ok) {
                responseDiv.textContent = `Bot: ${result.response}`;
            } else {
                responseDiv.textContent = `Error: ${result.error}`;
            }
        });
    </script>
</body>
</html>
"""

LOGS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Chat Logs</title>
</head>
<body>
    <h1>Chat Logs</h1>
    <table border="1">
        <tr>
            <th>Timestamp</th>
            <th>User</th>
            <th>User Input</th>
            <th>Bot Response</th>
        </tr>
        {% for log in logs %}
        <tr>
            <td>{{ log.timestamp }}</td>
            <td>{{ log.user_name }}</td>
            <td>{{ log.user_input }}</td>
            <td>{{ log.bot_response }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

# Save the templates
def save_template(file_path, content):
    # Ensure the directory exists
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Write content to the file
    with open(file_path, "w") as file:
        file.write(content)

# Save the HTML templates
save_template("templates/index.html", INDEX_HTML)
save_template("templates/logs.html", LOGS_HTML)

if __name__ == "__main__":
    # Create database tables within the application context
    with app.app_context():
        db.create_all()
    app.run(debug=True)
