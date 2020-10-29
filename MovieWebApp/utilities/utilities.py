from flask import Blueprint, request, render_template, redirect, url_for, session

import MovieWebApp.adapters.repository as repo
import MovieWebApp.utilities.services as services


# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)



# return a list of movies(dict)
def get_movies_top_20():
    movies = services.get_top_20_movies(repo.repo_instance)
    for movie in movies:
        movie['hyperlink'] = url_for('movies_bp.brows_movies', rank = movie['Rank'])
    return movies


# return a list of all movies(dict)
def get_all_movies():
    movies = services.get_all_movies(repo.repo_instance)
    for movie in movies:
        movie['hyperlink'] = url_for('movies_bp.brows_movies', rank = movie['Rank'])
    return movies


def get_first_movie():
    movie = services.get_first_movie(repo.repo_instance)
    movie['hyperlink'] = url_for('movies_bp.brows_movies', rank = movie['Rank'])
    return movie




