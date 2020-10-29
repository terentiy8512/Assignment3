import csv
import os

from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.security import generate_password_hash
import random

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from MovieWebApp.domain.model import User, Actor, Director, Genre, Movie, Review
from MovieWebApp.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()


    def get_user(self, username) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(user_name=username).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return user

    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()


    def get_review(self, find_review):
        review = None
        try:
            review = self._session_cm.session.query(Review).filter(Review.movie == find_review.movie).filter(Review.review_text == find_review.review_text).filter(Review.timestamp == find_review.timestamp).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return review

    def add_movie(self, movie: Movie):
        with self._session_cm as scm:
            scm.session.add(movie)
            scm.commit()


    def get_top_20_movies(self):
        top_20_movies = []
        try:
            top_20_movies = self._session_cm.session.query(Movie).limit(20).all()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return top_20_movies


    def get_all_movies(self):
        movies = self._session_cm.session.query(Movie).all()
        return movies


    def get_movie(self, movie_rank: int) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter(Movie.rank == movie_rank).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return movie


    def get_len_all_movies(self):
        len_of_movies = self._session_cm.session.query(Movie).count()
        return len_of_movies


    def get_rank_random_movies(self, quantity=5):
        movies_rank_list = []
        len_all_movies = self._session_cm.session.query(Movie).count()
        if len_all_movies >= quantity:
            for i in range(quantity):
                movies_rank_list.append(random.randint(1, len_all_movies))
        else:
            for movie in self._movies:
                movies_rank_list.append(random.randint(1, len_all_movies))
        return movies_rank_list


    def get_users(self):
        users = self._session_cm.session.query(User).all()
        return users
    '''
    def add_movie_to_watchlist(self, movie):
        with self._session_cm as scm:
            scm.session.add('INSERT INTO watch_lists (id, user_id, movie_rank) VALUES("5", "4", "1")')
            scm.commit()
    '''



def movie_generic_generator(filename):
    with open(filename, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)
        # Read first line of the CSV file.
        headers = next(reader)
        unwanted_parameters = [2, 4, 5, 9, 11]
        actor_id = 0
        genre_id = 0
        director_id = 0
        actors_added = list()
        genres_added = list()
        directors_added = list()
        # Read remaining rows from the CSV file.
        for row in reader:
            data = []

            director = row[4].strip()
            if director not in directors_added:
                director_id += 1
                directors_added.append(director)
                directors[row[0]] = [director_id, director]
                temp = director_id
            else:
                temp = directors_added.index(director) + 1


            counter = 0
            for element in row:
                element.strip()
                if counter not in unwanted_parameters:
                    data.append(element)
                elif counter == 4:
                    data.append(str(temp))
                counter += 1

            movies[row[0]] = list()
            actor_names = row[5].split(",")
            for actor in actor_names:
                actor_name = actor.strip()
                if actor_name not in actors_added:
                    actor_id += 1
                    actors_added.append(actor_name)
                    movies[row[0]].append([actor_id, actor_name])
                else:
                    actor_id_temp = actors_added.index(actor_name) + 1
                    movies[row[0]].append([actor_id_temp, actor_name])

            genres[row[0]] = list()
            genre_names = row[2].split(",")
            for genre in genre_names:
                genre_name = genre.strip()
                if genre_name not in genres_added:
                    genre_id += 1
                    genres_added.append(genre_name)
                    genres[row[0]].append([genre_id, genre_name])
                else:
                    genre_id_temp = genres_added.index(genre_name) + 1
                    genres[row[0]].append([genre_id_temp, genre_name])



            yield data


def get_actor_records():
    data = list()
    actors_added = list()
    actor_id = 0
    for key, value in movies.items():
        for id_name_pair in value:
            actor_name = id_name_pair[1]
            if actor_name not in actors_added:
                actor_id += 1
                actors_added.append(actor_name)
                data.append((actor_id, actor_name))
    return data


def movie_actor_generator():
    data = list()
    actors_added = list()
    id = 0
    movie_rank = 0
    for movie_rank in movies.keys():
        for id_name_pair in movies[movie_rank]:
            id += 1
            data.append((id, id_name_pair[0], movie_rank))
    return data


def get_genre_records():
    data = list()
    genres_added = list()
    genre_id = 0
    for key, value in genres.items():
        for id_name_pair in value:
            genre_name = id_name_pair[1]
            if genre_name not in genres_added:
                genre_id += 1
                genres_added.append(genre_name)
                data.append((genre_id, genre_name))
    return data


def movie_genre_generator():
    data = list()
    genres_added = list()
    id = 0
    movie_rank = 0
    for movie_rank in genres.keys():
        for id_name_pair in genres[movie_rank]:
            id += 1
            data.append((id, id_name_pair[0], movie_rank))
    return data


def get_directors():
    data = list()
    for key, value in directors.items():
        data.append((value[0], value[1]))
    return data


def generic_generator(filename, post_process=None):
    with open(filename) as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        next(reader)
        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            new_row = [item.strip() for item in row]
            if post_process is not None:
                watch_lists[int(row[0])] = list()
                row = post_process(row)
                new_row = new_row[0:3]
                movie_ranks = row[3].split()
                for movie_rank in movie_ranks:
                    watch_lists[int(row[0])].append(movie_rank)
            yield new_row


def get_watchlist():
    id = 0
    data = list()
    for user_id in watch_lists:
        for movie_rank in watch_lists[user_id]:
            id += 1
            data.append((id, user_id, int(movie_rank)))
    return data

def process_user(user_row):
    user_row[2] = generate_password_hash(user_row[2])
    return user_row


def populate(engine: Engine, data_path: str):
    conn = engine.raw_connection()
    cursor = conn.cursor()

    global movies
    movies = dict()

    global genres
    genres = dict()

    global directors
    directors = dict()

    global watch_lists
    watch_lists = dict()

    insert_movies = """
        INSERT INTO movies (
        rank, title, description, director_id, release_year, runtime_minutes, rating, revenue)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.executemany(insert_movies, movie_generic_generator(os.path.join(data_path, 'movies.csv')))


    insert_actors = """
        INSERT INTO actors (
        id, name)
        VALUES (?, ?)"""
    cursor.executemany(insert_actors, get_actor_records())


    insert_names_actors = """
        INSERT INTO actors_names (
        id, actor_id, movie_rank)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_names_actors, movie_actor_generator())


    insert_genres = """
        INSERT INTO genres (
        id, name)
        VALUES (?, ?)"""
    cursor.executemany(insert_genres, get_genre_records())


    insert_names_genres = """
        INSERT INTO genres_names (
        id, genre_id, movie_rank)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_names_genres, movie_genre_generator())


    insert_users = """
        INSERT INTO users (
        id, username, password)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_users, generic_generator(os.path.join(data_path, 'users.csv'), process_user))


    insert_watchlist = """
        INSERT INTO watch_lists (
        id, user_id, movie_rank)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_watchlist, get_watchlist())


    insert_reviews = """
        INSERT INTO reviews (
        user_id, movie_rank, review_text, rating, timestamp)
        VALUES (?, ?, ?, ?, ?)"""
    cursor.executemany(insert_reviews, generic_generator(os.path.join(data_path, 'reviews.csv')))


    insert_directors = """
        INSERT INTO directors (
        id, name)
        VALUES (?, ?)"""
    cursor.executemany(insert_directors, get_directors())


    conn.commit()
    conn.close()
