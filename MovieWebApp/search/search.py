
from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import MovieWebApp.adapters.repository as repo
import MovieWebApp.utilities.utilities as utilities
import MovieWebApp.search.services as services
from MovieWebApp.authentication.authentication import login_required


# Configure Blueprint.
search_blueprint = Blueprint(
    'search_bp', __name__)


@search_blueprint.route('/search_for_movie', methods=['GET', 'POST'])
def search_for_movie():

    search_category = request.args.get('category')

    current_page = request.args.get('page')

    search_string = request.args.get('search_string')

    form = SearchForm()

    if form.validate_on_submit():
        page = int(current_page)

        search_string = form.search_string.data
        result_list = None
        next_page = None
        prev_page = None

        if search_category == 'title':
            result_list = services.search_by_title_string(search_string, repo.repo_instance)

        if search_category == 'genre':
            result_list = services.search_by_genre_string(search_string, repo.repo_instance)

        if search_category == 'actor':
            result_list = services.search_by_actor_string(search_string, repo.repo_instance)

        if search_category == 'director':
            result_list = services.search_by_director_string(search_string, repo.repo_instance)

        if len(result_list) > page * 30:
            next_page = url_for(
                'search_bp.search_for_movie',
                category = search_category,
                page = str(page + 1),
                search_string = search_string
            )

        if page - 1 >= 1:
            prev_page = url_for(
                 'search_bp.search_for_movie',
                 category = search_category,
                 page = str(page - 1),
                 search_string = search_string
            )
        if 'username' in session:
            username = session['username']
            user_watch_list = services.get_watch_list(username, repo.repo_instance)
            result_list = services.check_for_user_watch_list(result_list, user_watch_list, repo.repo_instance)

        return render_template(
            'search/show_search.html',
            result_list = result_list,
            page = page,
            next_page = next_page,
            prev_page = prev_page,
            search_category = search_category,
            search_string = search_string,
            current_page = current_page
        )

    if request.method == 'GET' and current_page == '0':
        return render_template(
            'search/search.html',
            form=form,
            handler_url = url_for('search_bp.search_for_movie', category = search_category , page = '1', search_string = search_string),
            search_category = search_category,
            search_string = search_string,
            current_page = current_page
        )

    else:
        page = int(current_page)

        result_list = None
        next_page = None
        prev_page = None

        if search_category == 'title':
            result_list = services.search_by_title_string(search_string, repo.repo_instance)

        if search_category == 'genre':
            result_list = services.search_by_genre_string(search_string, repo.repo_instance)

        if search_category == 'actor':
            result_list = services.search_by_actor_string(search_string, repo.repo_instance)

        if search_category == 'director':
            result_list = services.search_by_director_string(search_string, repo.repo_instance)

        if result_list != None:
            if len(result_list) > page * 30:
                next_page = url_for(
                    'search_bp.search_for_movie',
                    category = search_category,
                    page = str(page + 1),
                    search_string = search_string
                )

            if page - 1 >= 1:
                prev_page = url_for(
                     'search_bp.search_for_movie',
                     category = search_category,
                     page = str(page - 1),
                     search_string = search_string
                )
        if 'username' in session:
            username = session['username']
            user_watch_list = services.get_watch_list(username, repo.repo_instance)
            result_list = services.check_for_user_watch_list(result_list, user_watch_list, repo.repo_instance)

        return render_template(
            'search/show_search.html',
            result_list = result_list,
            page = page,
            next_page = next_page,
            prev_page = prev_page,
            search_category = search_category,
            search_string = search_string,
            current_page = current_page
        )



@search_blueprint.route('/can_add_to_watchlist_search', methods=['GET', 'POST'])
@login_required
def add_to_watchlist_search():

    username = session['username']

    movie_rank = request.args.get('rank')

    search_category = request.args.get('category')

    current_page = request.args.get('page')

    search_string = request.args.get('search_string')

    movie = services.get_movie(int(movie_rank), repo.repo_instance)

    user = services.get_user(username, repo.repo_instance)

    user_watch_list = services.get_watch_list(username, repo.repo_instance)

    page = int(current_page)

    search_string = search_string
    result_list = None
    next_page = None
    prev_page = None

    if search_category == 'title':
        result_list = services.search_by_title_string(search_string, repo.repo_instance)

    if search_category == 'genre':
        result_list = services.search_by_genre_string(search_string, repo.repo_instance)

    if search_category == 'actor':
        result_list = services.search_by_actor_string(search_string, repo.repo_instance)

    if search_category == 'director':
        result_list = services.search_by_director_string(search_string, repo.repo_instance)

    if result_list != None:
        if len(result_list) > page * 30:
            next_page = url_for(
                'search_bp.search_for_movie',
                category = search_category,
                page = str(page + 1),
                search_string = search_string
            )

        if page - 1 >= 1:
            prev_page = url_for(
                 'search_bp.search_for_movie',
                 category = search_category,
                 page = str(page - 1),
                 search_string = search_string
            )

    if movie not in user_watch_list:
        user_watch_list = services.add_to_watchlist(username, movie, repo.repo_instance)
    else:
        user_watch_list = services.remove_movie_from_watchlist(int(movie_rank), username, repo.repo_instance)

    result_list = services.check_for_user_watch_list(result_list, user_watch_list, repo.repo_instance)


    return render_template(
        'search/show_search.html',
        result_list = result_list,
        page = page,
        next_page = next_page,
        prev_page = prev_page,
        search_category = search_category,
        search_string = search_string,
        current_page = current_page
    )




class SearchForm(FlaskForm):

    search_string = StringField('Search', [
        DataRequired()])
    submit = SubmitField('Search')
