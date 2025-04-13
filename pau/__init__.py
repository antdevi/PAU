import os
from flask import Flask
from .models.models import db
from .routes.chat_routes import chat_bp
from .routes.note_routes import notes_bp
from .routes.quiz_routes import quiz_bp
from .routes.progress_routes import progress_bp
from .routes.doittoday_routes import doittoday_bp
from .routes.auth_routes import auth_bp

 # ✅ Ensure this is imported

def create_app():
    basedir = os.path.abspath(os.path.dirname(__file__))

    app = Flask(__name__, 
                template_folder=os.path.join(basedir, "../public/templates"),
                static_folder=os.path.join(basedir, "../public/static"))
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../data/pau.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    app.register_blueprint(chat_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(notes_bp, url_prefix="/notes")
    app.register_blueprint(doittoday_bp, url_prefix='/openquiz')
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
