# test_memory_repository.py

# Imports.
from datetime import datetime
from MovieWebApp.domain.model import User, Actor, Director, Genre, Movie, Review
from MovieWebApp.adapters.repository import RepositoryException
import pytest


def test_repository_can_add_a_user(in_memory_repo):
    user = User('Dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('Dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_add_review(in_memory_repo):
    review = Review(Movie("Titanic", 1986), "Awesome movie!", 7.7)
    in_memory_repo.add_review(review)
    assert in_memory_repo.get_review(review) is review


def test_repository_can_retrieve_review_of_user(in_memory_repo):
    wanted_review = Review(Movie("Titanic", 1986), "Awesome movie!", 7.7)
    in_memory_repo.add_review(wanted_review)
    review = in_memory_repo.get_review(wanted_review)
    assert review == wanted_review


def test_repository_doesnt_add_same_review(in_memory_repo):
    review = Review(Movie("Guardians of the Galaxy", 2014), "Want to watch it again!", 9.5)
    in_memory_repo.add_review(review)
    assert len(in_memory_repo._reviews) == 5


def test_repository_can_add_a_movie(in_memory_repo):
    movie = Movie("Titanic", 1986)
    in_memory_repo.add_movie(movie)
    assert len(in_memory_repo._movies) == 10


def test_repository_can_retrieve_movie(in_memory_repo):
    wanted_movie = Movie("Guardians of the Galaxy", 2014)
    #rank of "Guardians of the Galaxy" movie is '1'
    movie = in_memory_repo.get_movie(1)
    assert movie == wanted_movie


def test_repository_doesnt_add_same_movie(in_memory_repo):
    movie = Movie("Guardians of the Galaxy", 2014)
    in_memory_repo.add_movie(movie)
    assert len(in_memory_repo._movies) == 9


def test_get_rank_random_movies(in_memory_repo):
    list = in_memory_repo.get_rank_random_movies()
    assert len(list) == 5