from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from ..forms import MovieReviewForm, SearchForm
from ..models import User, UserPasswords
from ..utils import current_time


passwords = Blueprint("passwords", __name__)


""" ************ View functions ************ """


@passwords.route("/", methods=["GET", "POST"])
def index():
    #The main user area. WHere you can add passwords/view them
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("movies.query_results", query=form.search_query.data))

    return render_template("index.html", form=form)


@passwords.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = movie_client.search(query)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("movies.index"))

    return render_template("query.html", results=results)


@passwords.route("/movies/<movie_id>", methods=["GET", "POST"])
def app_details(app_name):

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

    passwords = UserPasswords.objects.find()

    return render_template(
        "movie_detail.html", form=form, apps = passwords)


@passwords.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    reviews = Review.objects(commenter=user)

    return render_template("user_detail.html", username=username, reviews=reviews)
