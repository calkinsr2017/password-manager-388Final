from flask import Blueprint, redirect, url_for, render_template, flash, request, session
from flask_login import current_user, login_required, login_user, logout_user

from .. import bcrypt
from ..forms import RegistrationForm, LoginForm, UpdateMasterForm, SearchForm
from ..models import User

import qrcode.image.svg as svg
from io import BytesIO
import pyotp
import qrcode
from flask import Flask
from flask_mail import Mail
from flask_mail import Message

app = Flask(__name__)
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_ASCII_ATTACHMENTS = True,
    MAIL_USERNAME = 'thevault130@gmail.com',
    MAIL_PASSWORD = 'Vau!3L!ht@',
))

mail = Mail(app)

users = Blueprint("users", __name__)

""" ************ User Management views ************ """


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    search_form = SearchForm()

    if search_form.validate_on_submit():
        return redirect(url_for("passwords.search_query", app_name=search_form.search_query.data))

    master_form = UpdateMasterForm()

    if master_form.validate_on_submit():
        # current_user.username = username_form.username.data
        current_user.modify(username=master_form.username.data, email = master_form.email.data)
        current_user.save()

        msg = Message(
                subject = "Updated Email",
                sender="thevault130@gmail.com",
                recipients=[current_user.email],
                body = "You have succesfully updated your username and email for password manager!"
                )
        mail.send(msg)

        return redirect(url_for("users.account"))

    return render_template(
        "account.html",
        title="Account",
        master_form=master_form,
        search_form =search_form,
    )

@users.route("/qr_code")
def qr_code():
    if 'new_username' not in session:
        return redirect(url_for('passwords.index'))

    user = User.objects(username = session['new_username']).first()
    session.pop('new_username')

    uri = pyotp.totp.TOTP(user.otp_secret).provisioning_uri(name = user.username, issuer_name = 'Passwords-2FA')
    img = qrcode.make(uri, image_factory=svg.SvgPathImage)
    stream = BytesIO()
    img.save(stream)

    headers = {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0' 
    }

    return stream.getvalue(), headers

@users.route("/tfa")
def tfa():
    if 'new_username' not in session:
        return redirect(url_for("passwords.index"))

    headers = {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0' 
    }

    return render_template("2fa.html"), headers

@users.route("/register", methods=["GET", "POST"])
def register():
    #This needs to be at the loggin page
    if current_user.is_authenticated:
        return redirect(url_for("passwords.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        user.save()

        session['new_username'] = user.username
        msg = Message(
                subject = "Hello New User",
                sender="thevault130@gmail.com",
                recipients=[user.email],
                body = "Welcome to password manager, a website where you can store your passwords for your favorite apps and websites. \n \
                Please remember to download the OTP Authenticator app to be able to login to our website after registration."
                )
        mail.send(msg)
        return redirect(url_for("users.tfa"))

    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("passwords.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()

        if user is not None and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            login_user(user)
            return redirect(url_for("users.account"))
        else:
            flash("Login failed. Check your username and/or password")
            return redirect(url_for("users.login"))

    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("passwords.index"))

@users.route("/description")
def description():
    return render_template("description.html")
