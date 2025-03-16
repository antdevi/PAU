# app.py
import logging
from  pau import create_app # Adjust the import based on your package structure
from flask import Flask, render_template
import os

app = create_app()

app.secret_key = os.urandom(24)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/", methods=['GET'])
def home():
    app.logger.debug("Home route accessed")
    return render_template("auth.html")

@app.route("/revision")
def serve_revision():
    return render_template("revision.html")

@app.route('/doittoday')
def doittoday():
    return render_template("doittoday.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)