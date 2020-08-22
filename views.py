from flask import Blueprint, render_template, url_for, redirect, flash, request, jsonify
from time import localtime, strftime
import requests
from forms import *
from models import *
from application import login_manager, socketio, ROOMS, Config
from flask_socketio import send, join_room, leave_room
from flask_login import login_user, current_user, logout_user

main = Blueprint("main", __name__)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@main.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for("main.chat"))

    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Hash password
        hashed_password = pbkdf2_sha512.hash(password)
        if len(hashed_password) > 195:
            return redirect(url_for("main.home"))
        # Add to db
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Registered successfully. Please login!", "success")
        return redirect(url_for("main.login"))

    return render_template("index.html", title="Home", form=form, is_authenticated=current_user.is_authenticated)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_object = User.query.filter_by(username=form.username.data).first()
        login_user(user_object)
        return redirect(url_for("main.chat"))
    return render_template("login.html", title="Login", form=form, is_authenticated=current_user.is_authenticated)


@main.route('/chat', methods=['GET', 'POST'])
def chat():
    get_data_from_db("Lounge")
    if not current_user.is_authenticated:
        flash("Please login.", "danger")
        return redirect(url_for("main.login"))
    return render_template("chat.html", title="App", rooms=ROOMS, username=current_user.username,
                           is_authenticated=current_user.is_authenticated)


@main.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash("You have successfully logged out.", "success")
    return redirect(url_for("main.login"))


@main.route('/api/gif', methods=['GET', 'POST'])
def search_gif():
    query = request.args.get('query')
    if not query:
        query = "chicken"

    payload = {'s': query, 'api_key': Config.GIPHY_KEY, 'weirdness': 7}
    r = requests.get('http://api.giphy.com/v1/gifs/translate', params=payload)
    r = r.json()
    url = r['data']['images']['fixed_height_small']['url']
    return jsonify(url=url)


@socketio.on('message')
def message(data):
    send_message_to_db(data["room"], current_user.username, data["msg"], "msg")
    send({"msg": data["msg"], "username": current_user.username, "timestamp": strftime("%b-%d %I:%M%p", localtime())},
         room=data["room"])


@socketio.on('gif')
def send_gif(data):
    send_message_to_db(data["room"], current_user.username, data["url"], "url")
    send({"url": data["url"], "username": current_user.username}, room=data["room"])


@socketio.on('join')
def join(data):
    message_history_data = get_data_from_db(data["room"])
    message_history = []
    for msg in message_history_data:
        formatted = {"username": msg.username, "content": msg.content, "type": msg.type}
        message_history.append(formatted)
    print(message_history)
    message_to_send = current_user.username + " has joined the " + data["room"] + " room."

    join_room(data['room'])
    send({"msg": message_to_send, "message_history": message_history, "joiner": current_user.username}, room=data["room"])


@socketio.on('leave')
def leave(data):
    message_to_send = current_user.username + " has left the " + data["room"] + " room."
    leave_room(data['room'])
    send({"msg": message_to_send}, room=data["room"])


def send_message_to_db(room, username, content, type):
    db_message = Message(room=room, username=username, content=content, type=type)
    db.session.add(db_message)
    db.session.commit()


def get_data_from_db(room):
    data = Message.query.filter_by(room=room).order_by(Message.id).all()[-8:]
    return data
