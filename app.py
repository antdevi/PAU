from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from datetime import datetime
import os

# Flask application
app = Flask(__name__)

# Chatbot client setup
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# System instruction for the chatbot
system_instruction = {"role": "system", "content": "Always answer as mentor."}

# File to save chat logs
CHAT_LOG_FILE = "C:/Users/ANTARA DAS/Desktop/chat_log.txt"

# Ensure the directory exists
chat_log_dir = os.path.dirname(CHAT_LOG_FILE)
if chat_log_dir and not os.path.exists(chat_log_dir):
    os.makedirs(chat_log_dir)

# Function to save chat logs
def save_chat_log(user, user_input, bot_response):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CHAT_LOG_FILE, "a") as file:
        file.write(f"[{timestamp}] {user}: {user_input}\n")
        file.write(f"[{timestamp}] Bot: {bot_response}\n\n")

# Flask route for the chatbot interface
@app.route("/")
def index():
    return render_template("index.html")

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

        # Save the conversation to the log
        save_chat_log(user_name, user_input, bot_response)

        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Flask route to view chat logs
@app.route("/logs")
def view_logs():
    try:
        with open(CHAT_LOG_FILE, "r") as file:
            logs = file.readlines()
        return render_template("logs.html", logs=logs)
    except FileNotFoundError:
        return "No logs found.", 404

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
    <pre>
    {% for log in logs %}
    {{ log }}
    {% endfor %}
    </pre>
</body>
</html>
"""

# Save the HTML templates
with open("templates/index.html", "w") as f:
    f.write(INDEX_HTML)

with open("templates/logs.html", "w") as f:
    f.write(LOGS_HTML)

if __name__ == "__main__":
    app.run(debug=True)
