from datetime import date

import pytest

from MovieWebApp.authentication.services import AuthenticationException
from MovieWebApp.movies.services import NonExistentMovieException

from MovieWebApp.movies import services as movies_services
from MovieWebApp.authentication import services as auth_services
from MovieWebApp.search import services as search_services
from MovieWebApp.watchlist import services as watchlist_services



def test_can_add_user(in_memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', in_memory_repo)


def test_can_add_review(in_memory_repo):
    movie_rank = 1
    review_text = "Good movie"
    rating = 6.1
    username = 'fmercury'
    movies_services.add_review(movie_rank, review_text, rating, username, in_memory_repo)
    movie_reviews = movies_services.get_movie_reviews(movie_rank, in_memory_repo)
    assert len(movie_reviews) == 4


def test_does_not_add_review_to_non_existing_movie(in_memory_repo):
    movie_rank = 10
    review_text = "Good movie"
    rating = 6.1
    username = 'fmercury'
    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.add_review(movie_rank, review_text, rating, username, in_memory_repo)


def test_search_by_title_string(in_memory_repo):
   list_of_movies = search_services.search_by_title_string("gua", in_memory_repo)
   assert list_of_movies[0]["Title"] == "Guardians of the Galaxy"


def test_search_by_genre_string(in_memory_repo):
    list_of_movies = search_services.search_by_genre_string("action", in_memory_repo)
    assert len(list_of_movies) == 4


def test_search_by_actor_string(in_memory_repo):
    list_of_movies = search_services.search_by_actor_string('Vin Diesel', in_memory_repo)
    assert list_of_movies[0]["Actors"] == "Chris Pratt, Vin Diesel, Bradley Cooper, Zoe Saldana"


def test_search_by_director_string(in_memory_repo):
    list_of_movies = search_services.search_by_director_string("James Gunn", in_memory_repo)
    assert list_of_movies[0]["Title"] == "Guardians of the Galaxy"


def test_get_user_watchlist(in_memory_repo):
    username = 'fmercury'
    watchlist = watchlist_services.get_watch_list(username, in_memory_repo)
    assert len(watchlist) == 0