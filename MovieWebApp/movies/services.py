from typing import List, Iterable

from MovieWebApp.adapters.repository import AbstractRepository
from MovieWebApp.domain.model import  Movie, Review, Actor, Director, Genre, User


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass

def make_review(review_text: str, rating: float, user: User, movie: Movie):
    review = Review(movie, review_text, rating)
    user.add_review(review)
    return review


def add_review(movie_rank: int, review_text: str, rating: float, username: str, repo: AbstractRepository):
    # Check that the article exists.
    movie = repo.get_movie(movie_rank)
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create a review.
    review = make_review(review_text, round(rating, 2), user, movie)

    # Update the repository.
    repo.add_review(review)


def get_movie(movie_rank: int, repo: AbstractRepository):
    movie = repo.get_movie(movie_rank)
    if movie is None:
        raise NonExistentMovieException
    return movie_to_dict(movie)


def get_len_all_movies(repo: AbstractRepository):
    length = repo.get_len_all_movies()
    return length


def get_random_movies(repo: AbstractRepository):
    rank_list = []
    rank_list = repo.get_rank_random_movies()
    movies_list = []
    for rank in rank_list:
        movie = repo.get_movie(rank)
        if movie is None:
            raise NonExistentMovieException
        movies_list.append(movie)
    return movies_to_dict(movies_list)



def get_movie_reviews(movie_rank: int, repo: AbstractRepository):
    list_of_dict = []
    reviews = dict()
    users = repo.get_users()
    for user in users:
        user_reviews = user.reviews
        for review in user_reviews:
            reviewed_movie = review.movie
            rank = reviewed_movie.rank
            if int(rank) == int(movie_rank):
                reviews = {
                    'user': user.user_name,
                    'review text': review.review_text,
                    'time': review.timestamp,
                    'rating': review.rating
                }
                list_of_dict.append(reviews)
    return list_of_dict


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


def get_movie_object(movie_rank, repo: AbstractRepository):
    movie = repo.get_movie(movie_rank)
    if movie is None:
        raise NonExistentMovieException
    return movie


def get_user(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    return user


def remove_movie_from_watchlist(movie_rank: int, user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise NonExistentUserException
    movie = repo.get_movie(movie_rank)
    if movie in user.watch_list:
        index = user.watch_list.index(movie)
        user.watch_list.pop(index)
    return user.watch_list


def check_for_user_watch_list(movie, user_watch_list, repo: AbstractRepository):
    for movie1 in user_watch_list:
        if movie1.title == movie['Title']:
             movie['added_to_watchlist'] = "True"
    return movie



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