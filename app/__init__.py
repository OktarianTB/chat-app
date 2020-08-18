from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from app.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()
ROOMS = ["lounge", "news", "games", "coding"]


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    from app.views import main
    app.register_blueprint(main)
    return app

