from flask import Flask, redirect, url_for
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
    db.create_all()
    login_manager.init_app(app)
    socketio.init_app(app)

    from app.views import main
    app.register_blueprint(main)
    app.register_error_handler(404, page_not_found)

    from app.commands import create_tables
    app.cli.add_command(create_tables)

    return app


def page_not_found(e):
    return redirect(url_for("main.chat"))

