import pytest

from types import SimpleNamespace
import random
import string

from flask_app.forms import SearchForm, MovieReviewForm
from flask_app.models import User, Review


def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200

    search = SimpleNamespace(search_query="guardians", submit="Search")
    form = SearchForm(formdata=None, obj=search)
    response = client.post("/", data=form.data, follow_redirects=True)

    assert b"Guardians of the Galaxy" in response.data


@pytest.mark.parametrize(
    ("query", "message"), 
    (
        #Empty String
        ("", b"This field is required."),
        #short string
        ("g", b"Too many results"),
        #Random string
        ("ghfadgsasd", b"Movie not found"),
        #Too long
        ("HI"*51, b"Field must be between 1 and 100 characters long."),

    )
)
def test_search_input_validation(client, query, message):
    resp = client.get("/")

    search = SimpleNamespace(search_query=query, submit = "Search")
    form = SearchForm(formdata=None, obj=search)
    response = client.post("/", data = form.data, follow_redirects=True)

    assert message in response.data



def test_movie_review(client, auth):
    resp = client.get("/login")
    assert resp.status_code == 200
    auth.register()
    response = auth.login()

    with client: 
        guardians_id = "tt2015381"
        url = f"/movies/{guardians_id}"
        resp = client.get(url)

        assert resp.status_code == 200

        query = 'dvavfbareafkd'
        review = SimpleNamespace(text=query, submit="Enter Comment")
        form = MovieReviewForm(formdata=None, obj=review)
        response = client.post(url, data=form.data, follow_redirects=True)
        #print(response.data)
        assert b'dvavfbareafkd' in response.data 

        
        review = Review.objects(content=query).first()

        assert review is not None
    

    


#Weird ass errors are happening
@pytest.mark.parametrize(
    ("movie_id", "message"), 
    (
        ("short", b"Incorrect IMDb ID."),
        ("123456789", b"Incorrect IMDb ID."),
        ("123456789101", b"Incorrect IMDb ID."),
    )
)
def test_movie_review_redirects(client, movie_id, message):
    resp = client.get(f"/movies/")

    assert resp.status_code == 404 #how do you check that the 404 page came up?
    url = f"/movies/{movie_id}"
    resp = client.get(url)

    assert resp.status_code == 302
    resp = client.post(url, follow_redirects=True)
    
    assert message in resp.data



@pytest.mark.parametrize(
    ("comment", "message"), 
    (
        ("", b"This field is required"),
        ("a", b"Field must be between 5 and 500 characters long."),
        ("a"*502, b"Field must be between 5 and 500 characters long."),

    )
)
def test_movie_review_input_validation(client, auth, comment, message):
    resp = client.get("/login")
    assert resp.status_code == 200
    auth.register()
    response = auth.login()

    with client:
        guardians_id = "tt2015381"
        url = f"/movies/{guardians_id}"
        resp = client.get(url)

        assert resp.status_code == 200



        review = SimpleNamespace(text=comment, submit="Enter Comment")
        form = MovieReviewForm(formdata=None, obj=review)
        response = client.post(url, data=form.data, follow_redirects=True)

        assert message in response.data

