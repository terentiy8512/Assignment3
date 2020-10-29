from datetime import date, datetime

import pytest

from MovieWebApp.adapters.database_repository import SqlAlchemyRepository
from MovieWebApp.domain.model import User, Actor, Director, Genre, Movie, Review
from MovieWebApp.adapters.repository import RepositoryException

def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_movie_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_articles = repo.get_len_all_movies()

    # Check that the query returned 9 Movies.
    assert number_of_articles == 9


def test_get_rank_random_movies(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_rank_random_movies()

    assert len(movies) == 5

def test_get_users(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    users = repo.get_users()

    assert len(users) == 3

def test_get_all_movies(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_all_movies()

    assert len(movies) == 9