# app.py
import logging
from  pau import create_app # Adjust the import based on your package structure
from flask import render_template

app = create_app()

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def home():
    app.logger.debug("Home route accessed")
    return render_template("chat.html")

@app.route("/revision")
def serve_revision():
    return render_template("revision.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)