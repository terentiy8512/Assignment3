# memory_repository.py

# importing needed directories.
import csv
import os
from datetime import date, datetime
from werkzeug.security import generate_password_hash
import random

from MovieWebApp.adapters.repository import AbstractRepository, RepositoryException
from MovieWebApp.domain.model import User, Actor, Director, Genre, Movie, Review

########## Memory Repository. ##########

class MemoryRepository(AbstractRepository):

    def __init__(self):
        self._users = []
        self._movies = []
        self._reviews = []


    def add_user(self, user: User):
        if user not in self._users:
            self._users.append(user)


    def get_user(self, user_name) -> User:
        for user in self._users:
            if user.user_name.strip() == user_name.strip():
                return user
        return None


    def add_review(self, review: Review):
        if review not in self._reviews:
            self._reviews.append(review)


    def get_review(self, find_review):
        for review in self._reviews:
            if review == find_review:
                return review
        return None


    def add_movie(self, movie: Movie):
        if movie not in self._movies:
            self._movies.append(movie)


    def get_top_20_movies(self):
        top_20_movies = []
        if len(self._movies) >= 20:
            for i in range(20):
                top_20_movies.append(self._movies[i])
        else:
            for movie in self._movies:
                top_20_movies.append(movie)
        return top_20_movies


    def get_all_movies(self):
        return self._movies


    def get_movie(self, movie_rank: int) -> Movie:
        movie = None
        if (movie_rank - 1 >= 0 and movie_rank - 1 < len(self._movies)):
            movie = self._movies[movie_rank - 1]
        return movie


    def get_len_all_movies(self):
        return len(self._movies)


    def get_rank_random_movies(self, quantity=5):
        movies_rank_list = []
        if len(self._movies) >= quantity:
            for i in range(quantity):
                movies_rank_list.append(random.randint(1, (len(self._movies))))
        else:
            for movie in self._movies:
                movies_rank_list.append(random.randint(1, (len(self._movies))))
        return movies_rank_list


    def get_users(self):
        return self._users


    def add_review(self, review: Review):
        self._reviews.append(review)


########## Reading / Loading ##########


# read csv file with a given filename.
def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


# load movies to the repository.
def load_movies(data_path: str, repo: MemoryRepository):
    # dictionary of movies key(movie rank) = value(Movie object).
    movies = dict()

    # creating the movie object from the file and adding to repository.
    for data_row in read_csv_file(os.path.join(data_path, 'movies.csv')):
        movie = Movie(title = data_row[1], release_year = int(data_row[6]))

        movie.director = Director(data_row[4].strip())
        movie.rank = data_row[0]
        movie.runtime_minutes = int(data_row[7])
        movie.rating = float(data_row[8])
        movie.add_revenue = data_row[10]
        movie.description = data_row[3]
        movie.revenue = data_row[10]

        # adding actors.
        actors_fullname = []
        actors_fullname = data_row[5].split(',')
        list_of_actors = []
        for fullname in actors_fullname:
            actor = Actor(fullname.strip())
            list_of_actors.append(actor)
            movie.add_actor(actor)

        # adding colleagues.
        for main_actor in list_of_actors:
            for colleague in list_of_actors:
                if (not main_actor.check_if_this_actor_worked_with(colleague)) and (main_actor != colleague):
                    main_actor.add_actor_colleague(colleague)

        # adding genres.
        genres = []
        genres = data_row[2].split(',')
        for genre_name in genres:
            genre = Genre(genre_name.strip())
            movie.add_genre(genre)

        # adding movie to the repository.
        repo.add_movie(movie)
        movies[data_row[0]] = movie
    return movies


# load users to the repository.
def load_users(data_path: str, repo: MemoryRepository, movies):
    # dictionary of users, key(id) = value(User object).
    users = dict()

    # creating User object from the file and adding to repository.
    for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
        user = User(user_name = data_row[1], password = generate_password_hash(data_row[2]))

        # adding watched movies and watchlist.
        all_movies = data_row[3].split()
        for movie_rank in all_movies:
            movie = movies[movie_rank]
            user.watch_movie(movie)
            user.add_to_watch_list(movie)
        repo.add_user(user)
        users[data_row[0]] = user
    return users


# load reviews to the repository
def load_reviews(data_path: str, repo: MemoryRepository, users, movies):
    for data_row in read_csv_file(os.path.join(data_path, 'reviews.csv')):
        review = Review(
            movie = movies[data_row[1]],
            review_text = data_row[2],
            rating = float(data_row[3]),
            timestamp = datetime.fromisoformat(data_row[4])
        )
        user = users[data_row[0]]
        user.add_review(review)
        repo.add_review(review)


def populate(data_path: str, repo: MemoryRepository):
    # Load articles and tags into the repository.
    movies = load_movies(data_path, repo)

    # Load users into the repository.
    users = load_users(data_path, repo, movies)

    # Load reviews into the repository.
    load_reviews(data_path, repo, users, movies)