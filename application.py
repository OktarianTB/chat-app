from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from config import Config


def page_not_found(e):
    return redirect(url_for("main.chat"))


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

socketio = SocketIO()
socketio.init_app(app)

ROOMS = ["lounge", "news", "games", "coding"]

from views import main
app.register_blueprint(main)
app.register_error_handler(404, page_not_found)

if __name__ == "__main__":
    print("Running flask app!")
    app.run()
