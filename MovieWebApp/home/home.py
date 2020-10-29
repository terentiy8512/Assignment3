
from MovieWebApp.authentication.authentication import login_required
import MovieWebApp.utilities.utilities as utilities
import MovieWebApp.utilities.services as services
import MovieWebApp.adapters.repository as repo

from flask import Blueprint, request, render_template, redirect, url_for, session


home_blueprint = Blueprint('home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():

    top_20_movies = utilities.get_movies_top_20()

    if 'username' in session:

        username = session['username']
        user_watch_list = services.get_watch_list(username, repo.repo_instance)

        top_20_movies = services.check_for_user_watch_list(top_20_movies, user_watch_list, repo.repo_instance)

    return render_template(
        'home/home.html',
        top_20_movies = top_20_movies,
        first_movie = utilities.get_first_movie()
    )


@home_blueprint.route('/can_add_to_watchlist', methods=['GET', 'POST'])
@login_required
def add_to_watchlist():

    username = session['username']

    movie_rank = request.args.get('rank')

    movie = services.get_movie(int(movie_rank), repo.repo_instance)

    user = services.get_user(username, repo.repo_instance)

    user_watchlist = services.get_watch_list(username, repo.repo_instance)

    top_20_movies = utilities.get_movies_top_20()

    first_movie = utilities.get_first_movie()

    if movie not in user_watchlist:
        user_watch_list = services.add_to_watchlist(username, movie, repo.repo_instance)
    else:
        user_watch_list = services.remove_movie_from_watchlist(int(movie_rank), username, repo.repo_instance)

    top_20_movies = services.check_for_user_watch_list(top_20_movies, user_watch_list, repo.repo_instance)


    return render_template(
        'home/home.html',
        top_20_movies = top_20_movies,
        first_movie = first_movie
    )




