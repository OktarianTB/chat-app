from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from app.models import User
from passlib.hash import pbkdf2_sha512


def invalid_credentials(form, field):
    username_entered = form.username.data
    password_entered = field.data
    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None:
        raise ValidationError("Username or password incorrect")
    elif not pbkdf2_sha512.verify(password_entered, user_object.password):
        raise ValidationError("Username or password incorrect")


class RegistrationForm(FlaskForm):
    username = StringField("username", validators=[InputRequired(message="Username is required"),
                                                   Length(min=4, max=20, message="Username must be between "
                                                                                 "4 and 20 characters")])
    password = PasswordField('password', validators=[InputRequired(message="Password is required"),
                                                     Length(min=4, max=20, message="Password must be between "
                                                                                   "4 and 20 characters")])
    password_confirm = PasswordField('password_confirm',
                                     validators=[InputRequired(message="Password Confirmation is required"),
                                                 EqualTo("password", message="Passwords must match")])
    submit = SubmitField("Create")

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username already exists")


class LoginForm(FlaskForm):
    username = StringField("username", validators=[InputRequired(message="Username is required")])
    password = PasswordField("password", validators=[InputRequired(message="Password is required"), invalid_credentials])
    submit = SubmitField("Login")
