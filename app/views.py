from flask import Blueprint, render_template, url_for, redirect, flash
from time import localtime, strftime
from app.forms import *
from app.models import *
from app import login_manager, socketio, ROOMS
from flask_socketio import send, join_room, leave_room
from flask_login import login_user, current_user, logout_user

main = Blueprint("main", __name__)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@main.route('/', methods=['GET', 'POST'])
def home():
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

    return render_template("index.html", title="Home", form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_object = User.query.filter_by(username=form.username.data).first()
        login_user(user_object)
        return redirect(url_for("main.chat"))
    return render_template("login.html", title="Login", form=form)


@main.route('/chat', methods=['GET', 'POST'])
def chat():
    if not current_user.is_authenticated:
        flash("Please login.", "danger")
        return redirect(url_for("main.login"))
    return render_template("chat.html", rooms=ROOMS, username=current_user.username)


@main.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash("You have successfully logged out.", "success")
    return redirect(url_for("main.login"))


@socketio.on('message')
def message(data):
    send({"msg": data["msg"], "username": current_user.username, "timestamp": strftime("%b-%d %I:%M%p", localtime())},
         room=data["room"])


@socketio.on('join')
def join(data):
    join_room(data['room'])
    send({"msg": current_user.username + " has joined the " + data["room"] + " room."}, room=data["room"])


@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({"msg": current_user.username + " has left the " + data["room"] + " room."}, room=data["room"])

