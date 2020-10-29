from MovieWebApp.adapters.repository import AbstractRepository
from MovieWebApp.domain.model import  Movie, Review, Actor, Director, Genre, User
from typing import List, Iterable


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def search_by_title_string(search_string: str, repo: AbstractRepository):
    all_movies = repo.get_all_movies()
    output_list_of_movies = []
    for movie in all_movies:
        title = movie.title.lower()
        if search_string.lower() in title:
            output_list_of_movies.append(movie)

    output_list_of_movies = movies_to_dict(output_list_of_movies)
    page = 1
    if len(output_list_of_movies) > 30:
        for index in range (1, len(output_list_of_movies) + 1):
            output_list_of_movies[index - 1]['page'] = page
            if index % 30 == 0:
                page += 1
    return output_list_of_movies



def search_by_genre_string(search_string: str, repo: AbstractRepository):
    all_movies = repo.get_all_movies()
    output_list_of_movies = []
    for movie in all_movies:
        genres = movie.genres
        for genre in genres:
            if search_string.lower() in genre.genre_name.lower():
                output_list_of_movies.append(movie)
                break

    output_list_of_movies = movies_to_dict(output_list_of_movies)
    page = 1
    if len(output_list_of_movies) > 30:
        for index in range (1, len(output_list_of_movies) + 1):
            output_list_of_movies[index - 1]['page'] = page
            if index % 30 == 0:
                page += 1
    return output_list_of_movies


def search_by_actor_string(search_string: str, repo: AbstractRepository):
    all_movies = repo.get_all_movies()
    output_list_of_movies = []
    for movie in all_movies:
        actors = movie.actors
        for actor in actors:
            if search_string.lower() in actor.actor_full_name.lower():
                output_list_of_movies.append(movie)
                break

    output_list_of_movies = movies_to_dict(output_list_of_movies)
    page = 1
    if len(output_list_of_movies) > 30:
        for index in range (1, len(output_list_of_movies) + 1):
            output_list_of_movies[index - 1]['page'] = page
            if index % 30 == 0:
                page += 1
    return output_list_of_movies



def search_by_director_string(search_string: str, repo: AbstractRepository):
    all_movies = repo.get_all_movies()
    output_list_of_movies = []
    for movie in all_movies:
        director = movie.director
        if search_string.lower() in director.director_full_name.lower():
            output_list_of_movies.append(movie)

    output_list_of_movies = movies_to_dict(output_list_of_movies)
    page = 1
    if len(output_list_of_movies) > 30:
        for index in range (1, len(output_list_of_movies) + 1):
            output_list_of_movies[index - 1]['page'] = page
            if index % 30 == 0:
                page += 1
    return output_list_of_movies


def get_movie(movie_rank: int, repo: AbstractRepository):
    movie = repo.get_movie(movie_rank)
    if movie is None:
        raise NonExistentMovieException
    return movie


def get_user(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    return user


def get_watch_list(user_name: str, repo: AbstractRepository):
    user_watch_list = []
    user = repo.get_user(user_name)
    user_watch_list = user.watch_list
    return user_watch_list


def add_to_watchlist(user_name: str, movie: Movie, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise NonExistentUserException
    if movie not in user.watch_list:
        user.watch_list.append(movie)
    return user.watch_list


def remove_movie_from_watchlist(movie_rank: int, user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise NonExistentUserException
    movie = repo.get_movie(movie_rank)
    if movie in user.watch_list:
        index = user.watch_list.index(movie)
        user.watch_list.pop(index)
    return user.watch_list


def check_for_user_watch_list(result_list, user_watch_list, repo: AbstractRepository):
    for movie_dict in result_list:
        for movie in user_watch_list:
            if movie.title == movie_dict['Title']:
                movie_dict['added_to_watchlist'] = "True"
    return result_list

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
        'added_to_watchlist': "False",
        'page': 1
    }
    return movie_dict

def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]