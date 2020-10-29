from typing import Iterable
import random

from MovieWebApp.adapters.repository import AbstractRepository
from MovieWebApp.domain.model import  Movie, Review, Actor, Director, Genre, User


class NonExistentMovieException(Exception):
    pass


class NonExistentUserException(Exception):
    pass


# function returns dictionary of movies
def get_top_20_movies(repo: AbstractRepository):
    movies = repo.get_top_20_movies()
    return movies_to_dict(movies)


def get_all_movies(repo: AbstractRepository):
    movies = repo.get_all_movies()
    return movies_to_dict(movies)


def get_first_movie(repo: AbstractRepository):
    movie = repo.get_movie(1)
    if movie is None:
        raise NonExistentMovieException
    return movie_to_dict(movie)


def get_movie(movie_rank: int, repo: AbstractRepository):
    movie = repo.get_movie(movie_rank)
    if movie is None:
        raise NonExistentMovieException
    return movie


def get_user(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise NonExistentUserException
    return user


def add_to_watchlist(user_name: str, movie: Movie, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise NonExistentUserException
    if movie not in user.watch_list:
        user.watch_list.append(movie)
        #repo.add_movie_to_watchlist(movie)
    return user.watch_list


def get_watch_list(user_name: str, repo: AbstractRepository):
    user_watch_list = []
    user = repo.get_user(user_name)
    if user is None:
        raise NonExistentUserException
    user_watch_list = user.watch_list
    return user_watch_list


def check_for_user_watch_list(top_20_movies, user_watch_list, repo: AbstractRepository):
    for movie_dict in top_20_movies:
        for movie in user_watch_list:
            if movie.title == movie_dict['Title']:
                movie_dict['added_to_watchlist'] = "True"
    return top_20_movies


def remove_movie_from_watchlist(movie_rank: int, user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise NonExistentUserException
    movie = repo.get_movie(movie_rank)
    if movie in user.watch_list:
        index = user.watch_list.index(movie)
        user.watch_list.pop(index)
    return user.watch_list




# ============================================
# Functions to convert dicts to model entities
# ============================================

def movie_to_dict(movie: Movie):
    genre_str = ""
    for genre in  movie.genres:
        genre_str += genre.genre_name
        genre_str += ", "
    genre_str = genre_str[0: len(genre_str) - 2]

    actor_str = ""
    for actor in movie.actors:
        actor_str += actor.actor_full_name
        actor_str += ", "
    actor_str = actor_str[0: len(actor_str) - 2]

    movie_dict = {
        'Title': movie.title,
        'Director': movie.director.director_full_name,
        'Description': movie.description,
        'Rating': movie.rating,
        'Rank': movie.rank,
        'Release year': movie.release_year,
        'Revenue': str(movie.revenue) + " millions",
        'Actors': actor_str,
        'Genres': genre_str,
        'Runtime': str(movie.runtime_minutes) + " minutes",
        'added_to_watchlist': "False"
    }
    return movie_dict

def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]