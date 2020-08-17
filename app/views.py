from flask import Blueprint, render_template, url_for, redirect
from app.forms import *
from app.models import *
from app import login_manager
from flask_login import login_user, current_user, login_required, logout_user

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
@login_required
def chat():
    return "Chat with me"


@main.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for("main.login"))