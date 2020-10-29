# repository.py

# imports.
import abc
from datetime import datetime
from MovieWebApp.domain.model import User, Actor, Director, Genre, Movie, Review


repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass

# abstract class for repository.
class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """ Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """
            Returns the User with specified username, if there is no User
            with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review, username):
        """ Adds a new review to the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_review(self):
        """ Returns a specified review. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """ Adds a movie to the repository. """
        raise NotImplementedError


    @abc.abstractmethod
    def get_top_20_movies(self):
        """ Returns list of top 20 movies """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_movies(self):
        """ Returns list of movies """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, movie_rank):
        """ Returns movie by its rank """
        raise NotImplementedError

    @abc.abstractmethod
    def get_len_all_movies(self):
        """ Returns length of self._movies """
        raise NotImplementedError

    @abc.abstractmethod
    def get_rank_random_movies(self, quantity: int):
        """ Returns random movies """
        raise NotImplementedError

    @abc.abstractmethod
    def get_users(self):
        """ Returns list of users """
        raise NotImplementedError


    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Review to the repository. """
        raise NotImplementedError


