from MovieWebApp.adapters.repository import AbstractRepository
from MovieWebApp.domain.model import  Movie, Review, Actor, Director, Genre, User


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def get_watch_list(user_name: str, repo: AbstractRepository):
    user_watch_list = []
    user = repo.get_user(user_name)
    user_watch_list = user.watch_list
    return user_watch_list


def check_for_user_watch_list(movie, user_watch_list, repo: AbstractRepository):
    for movie1 in user_watch_list:
        if movie1.title == movie['Title']:
             movie['added_to_watchlist'] = "True"
    return movie