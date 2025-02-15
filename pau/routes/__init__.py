import os
from flask import Flask, render_template

# ✅ Import blueprints
from pau.routes.chat_routes import chat_bp
from pau.routes.note_routes import notes_bp
from pau.routes.quiz_routes import quiz_bp
from pau.routes.progress_routes import progress_bp


def create_app():
    basedir = os.path.abspath(os.path.dirname(__file__))

    # ✅ Initialize Flask app with proper directories
    app = Flask(__name__, 
                template_folder=os.path.join(basedir, "../public/templates"),
                static_folder=os.path.join(basedir, "../public/static"))

    # ✅ Register blueprints
    app.register_blueprint(chat_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(notes_bp, url_prefix="/notes")
    
    return app
