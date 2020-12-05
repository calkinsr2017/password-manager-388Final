from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from .. import bcrypt
from ..forms import RegistrationForm, LoginForm, UpdateMasterForm, SearchForm
from ..models import User


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
        current_user.modify(username=master_form.username.data, password = master_form.password.data)
        current_user.save()
        return redirect(url_for("users.account"))

    return render_template(
        "account.html",
        title="Account",
        master_form=master_form,
        search_form =search_form,
    )


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

        return redirect(url_for("users.login"))

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

