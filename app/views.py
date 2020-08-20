from flask import Blueprint, render_template, url_for, redirect, flash, request, jsonify
from time import localtime, strftime
import requests
from app.forms import *
from app.models import *
from app import login_manager, socketio, ROOMS, Config
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
    db_message = Message(room=data["room"], username=current_user.username, content=data["msg"], type="msg")
    db.session.add(db_message)
    db.session.commit()
    send({"msg": data["msg"], "username": current_user.username, "timestamp": strftime("%b-%d %I:%M%p", localtime())},
         room=data["room"])


@socketio.on('gif')
def send_gif(data):
    db_message = Message(room=data["room"], username=current_user.username, content=data["url"], type="url")
    db.session.add(db_message)
    db.session.commit()
    send({"url": data["url"], "username": current_user.username}, room=data["room"])


@socketio.on('join')
def join(data):
    message_to_send = current_user.username + " has joined the " + data["room"] + " room."
    db_message = Message(room=data["room"], username=current_user.username, content=message_to_send, type="info")
    db.session.add(db_message)
    db.session.commit()
    join_room(data['room'])
    send({"msg": message_to_send}, room=data["room"])


@socketio.on('leave')
def leave(data):
    message_to_send = current_user.username + " has left the " + data["room"] + " room."
    db_message = Message(room=data["room"], username=current_user.username, content=message_to_send, type="info")
    db.session.add(db_message)
    db.session.commit()
    leave_room(data['room'])
    send({"msg": message_to_send}, room=data["room"])

