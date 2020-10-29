# test_domain_model.py

# Imports.
from datetime import datetime
from MovieWebApp.domain.model import User, Actor, Director, Genre, Movie, Review
import pytest


@pytest.fixture()
def user():
    return User("vreg113", "1234567890")

@pytest.fixture()
def movie():
    return Movie("Titanic", 1986)

@pytest.fixture()
def review():
    return Review(Movie("Titanic", 1986), "Awesome movie!", 7.7)

def test_user_construction(user):
    assert user.user_name == 'vreg113'
    assert user.password == '1234567890'
    assert repr(user) == '<User vreg113>'
    assert user.time_spent_watching_movies_minutes == 0
    for review in user.reviews:
        # User should not have any reviews after construction.
        assert False
    for movie in user.watched_movies:
        # User should not have any watched movies after construction.
        assert False


def test_movie_after_construction(movie):
    assert movie._title == 'Titanic'
    assert movie._release_year == 1986
    assert movie.description == ''
    assert movie.rank == 0
    assert movie.rating == 0
    assert repr(movie) == '<Movie Titanic, 1986>'


def test_review_after_construction(review):
    assert review.movie == Movie("Titanic", 1986)
    now = datetime.now()
    timestamp = now.strftime("%c")
    assert repr(review) == '<Movie Titanic, 1986>, Review: Awesome movie!, Rating: 7.7, Time: ' + str(timestamp)
    assert review.review_text == "Awesome movie!"


def test_make_review(user):
    review = Review(Movie("Titanic", 1986), "Awesome movie!", 7.7)
    user.add_review(review)
    assert len(user.reviews) == 1
    user.add_review(review)
    assert len(user.reviews) == 1


def test_movie(movie):
    movie.add_actor(Actor("khan Solo"))
    movie.add_actor(Actor("Anieken Skywalker"))
    movie.add_actor(Actor("Yoda"))
    assert len(movie.actors) == 3
    movie.remove_actor(Actor("Yoda"))
    assert len(movie.actors) == 2
    assert Actor("Yoda").actor_full_name == "Yoda"
    movie.add_genre("Adventure")
    assert len(movie.genres) == 1
    movie.remove_genre("Adventure")
    assert len(movie.genres) == 0
    movie.director = Director("Face")
    assert movie.director.director_full_name == "Face"
    movie.description = "Star Wars"
    assert movie.description == "Star Wars"