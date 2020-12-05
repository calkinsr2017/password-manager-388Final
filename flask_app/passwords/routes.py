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
        return redirect(url_for("passwords.query_results", query=form.search_query.data))

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
def movie_detail(movie_id):
    try:
        result = movie_client.retrieve_movie_by_id(movie_id)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("users.login"))

    form = MovieReviewForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            imdb_id=movie_id,
            movie_title=result.title,
        )
        review.save()

        return redirect(request.path)

    reviews = Review.objects(imdb_id=movie_id)

    return render_template(
        "movie_detail.html", form=form, movie=result, reviews=reviews
    )


@passwords.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    reviews = Review.objects(commenter=user)

    return render_template("user_detail.html", username=username, reviews=reviews)
