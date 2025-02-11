import os
from flask import Flask
from .routes.chat_routes import chat_bp
from .routes.note_routes import notes_bp


 # ✅ Ensure this is imported

def create_app():
    basedir = os.path.abspath(os.path.dirname(__file__))

    app = Flask(__name__, 
                template_folder=os.path.join(basedir, "../public/templates"),
                static_folder=os.path.join(basedir, "../public/static"))
    app.register_blueprint(chat_bp)
    
    app.register_blueprint(notes_bp, url_prefix="/notes")


    return app
