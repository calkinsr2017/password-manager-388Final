from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
)

import pyotp
from .models import User
from .utils import *

class SearchForm(FlaskForm):
    search_query = StringField(
        "App Name", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("Search")


class PasswordForm(FlaskForm):
    app = StringField(
        "App", validators=[InputRequired()])
    appLink = StringField("AppLink")
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Submit")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")
    
    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")

    def validate_password(self, password):
        if not verifyPassword(str(password.data)):
            raise ValidationError("Password must contain an uppercase letter, a number, and a special char")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

    token = StringField('Token', validators=[InputRequired(), Length(min=6, max=6)])

    def validate_token(self, token):
        user = User.objects(username=self.username.data).first()
        if user is not None:
            tok_verified = pyotp.TOTP(user.otp_secret).verify(token.data)
            if not tok_verified:
                raise ValidationError("Invalid Token")


class UpdateMasterForm(FlaskForm):
    username = StringField(
        "Username", validators=[ Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[ Email()])
    submit = SubmitField("Update Username")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.objects(username=username.data).first()
            if user is not None:
                raise ValidationError("That username is already taken")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.objects(email=email.data).first()
            if user is not None:
                raise ValidationError("Email is already taken")

class DuoAuthenticationForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    submit = SubmitField("Authenticate!")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")
