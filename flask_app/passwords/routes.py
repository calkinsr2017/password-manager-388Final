from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from ..forms import PasswordForm, SearchForm
from ..models import User, UserPasswords
from ..utils import current_time


passwords = Blueprint("passwords", __name__)


""" ************ View functions ************ """


@passwords.route("/", methods=["GET", "POST"])
def index():
    #The main user area. WHere you can add passwords/view them
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("passwords.search-results", app_name=form.search_app.data))

    return render_template("index.html", form=form)


@passwords.route("/search-results/<app_name>", methods=["GET", "POST"])
def search_query(app_name):

    results = UserPasswords.objects(app = app_name)

    return render_template("query.html", results=results)

@passwords.route("/apps", methods=["GET", "POST"])
def app_details():

    form = PasswordForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        password = UserPasswords(
            user = current_user._get_current_object(), 
            app = form.app.data, 
            appLink = form.appLink.data, 
            username = form.username.data, 
            password = form.password.data,
        )
        password.save()

        return redirect(request.path)

    passwords = UserPasswords.objects.all()

    return render_template(
        "app_details.html", form=form, passwords = passwords)


@passwords.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    passwords = UserPasswords.objects(user=user)

    return render_template("user_detail.html", username=username, passwords=passwords)
