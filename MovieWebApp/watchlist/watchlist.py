from MovieWebApp.authentication.authentication import login_required

import MovieWebApp.utilities.services as utilities
import MovieWebApp.watchlist.services as services
import MovieWebApp.adapters.repository as repo

from flask import Blueprint, request, render_template, redirect, url_for, session
from MovieWebApp.authentication.authentication import login_required

watchlist_blueprint = Blueprint('watchlist_bp', __name__)


@watchlist_blueprint.route('/watchlist', methods=['GET'])
@login_required
def watchlist():
    username = session['username']

    watchlist_list = services.get_watch_list(username, repo.repo_instance)

    watchlist_dict = utilities.movies_to_dict(watchlist_list)

    for movie_dict in watchlist_dict:
        movie_dict = services.check_for_user_watch_list(movie_dict, watchlist_list, repo.repo_instance)
        movie_dict['hyperlink'] = url_for('movies_bp.brows_movies', rank = movie_dict['Rank'])

    if len(watchlist_dict) == 0:
        watchlist_dict = None

    return render_template(
        'watchlist/watchlist.html',
        watchlist = watchlist_dict
    )



@watchlist_blueprint.route('/remove_from_watchlist', methods=['GET'])
@login_required
def remove_from_watchlist():

    username = session['username']
    movie_rank = request.args.get('rank')

    movie = utilities.get_movie(int(movie_rank), repo.repo_instance)

    user_watchlist = services.get_watch_list(username, repo.repo_instance)

    user_watchlist = utilities.remove_movie_from_watchlist(int(movie_rank), username, repo.repo_instance)

    user_watchlist_dict = utilities.movies_to_dict(user_watchlist)

    for movie_dict in user_watchlist_dict:
        movie_dict = services.check_for_user_watch_list(movie_dict, user_watchlist, repo.repo_instance)
        movie_dict['hyperlink'] = url_for('movies_bp.brows_movies', rank = movie_dict['Rank'])

    if len(user_watchlist_dict) == 0:
        user_watchlist_dict = None

    return render_template(
        'watchlist/watchlist.html',
        watchlist = user_watchlist_dict
    )
