import os
from flask import Flask
from .routes.chat_routes import chat_bp
from .routes.note_routes import notes_bp
from .routes.quiz_routes import quiz_bp
from .routes.progress_routes import progress_bp
from .routes.doittoday_routes import doittoday_bp

 # ✅ Ensure this is imported

def create_app():
    basedir = os.path.abspath(os.path.dirname(__file__))

    app = Flask(__name__, 
                template_folder=os.path.join(basedir, "../public/templates"),
                static_folder=os.path.join(basedir, "../public/static"))
    app.register_blueprint(chat_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(notes_bp, url_prefix="/notes")
    app.register_blueprint(doittoday_bp, url_prefix='/openquiz')

    return app
