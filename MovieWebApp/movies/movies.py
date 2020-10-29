from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired, AnyOf

import MovieWebApp.adapters.repository as repo
import MovieWebApp.utilities.utilities as utilities
import MovieWebApp.movies.services as services

from MovieWebApp.authentication.authentication import login_required

# Configure Blueprint.
movies_blueprint = Blueprint(
    'movies_bp', __name__)


@movies_blueprint.route('/brows_movies', methods=['GET', 'POST'])
def brows_movies():

    target_movie_rank = request.args.get('rank')

    current_movie = services.get_movie(int(target_movie_rank), repo.repo_instance)

    total_movies = services.get_len_all_movies(repo.repo_instance)


    random_movies = services.get_random_movies(repo.repo_instance)

    for movie in random_movies:
        movie['hyperlink'] = url_for('movies_bp.brows_movies', rank = movie['Rank'])

    prev_movie_url = None
    next_movie_url = None

    if (int(target_movie_rank) - 1 > 0):
        prev_movie_url = url_for('movies_bp.brows_movies', rank = (int(target_movie_rank) - 1))

    if (int(target_movie_rank) + 1 <= total_movies):
        next_movie_url = url_for('movies_bp.brows_movies', rank = (int(target_movie_rank) + 1))


    current_movie['add_review_url'] = url_for('movies_bp.make_review_for_movie', rank = current_movie['Rank'])

    reviews = services.get_movie_reviews(int(target_movie_rank), repo.repo_instance)

    if len(reviews) == 0:
        reviews = None


    if 'username' in session:
        username = session['username']

        user_watch_list = services.get_watch_list(username, repo.repo_instance)

        current_movie = services.check_for_user_watch_list(current_movie, user_watch_list, repo.repo_instance)


    return render_template(
        'movies/movies.html',
        title='Movies',
        current_movie = current_movie,
        random_movies = random_movies,
        prev_movie_url = prev_movie_url,
        next_movie_url = next_movie_url,
        reviews = reviews
    )


@movies_blueprint.route('/make_review', methods=['GET', 'POST'])
@login_required
def make_review_for_movie():
    # Obtain the username of the currently logged in user.
    username = session['username']

    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the review text has passed data validation.
        # Extract the movie rank, representing the movie review, from the form.
        movie_rank = int(form.movie_rank.data)

        services.add_review(movie_rank, form.review.data, form.rating.data, username, repo.repo_instance)
        current_movie = services.get_movie(movie_rank, repo.repo_instance)

        return redirect(url_for('movies_bp.brows_movies', rank = current_movie['Rank']))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the movie rank, representing the movie to review, from a query parameter of the GET request.
        movie_rank = int(request.args.get('rank'))

        # Store the movie rank in the form.
        form.movie_rank.data = movie_rank
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the movie rank of the movie being reviewed from the form.
        movie_rank = int(form.movie_rank.data)

    # For a GET or an unsuccessful POST, retrieve the movie to review in dict form, and return a Web page that allows
    # the user to enter a review. The generated Web page includes a form object.
    current_movie = services.get_movie(movie_rank, repo.repo_instance)

    reviews = services.get_movie_reviews(int(movie_rank), repo.repo_instance)
    if len(reviews) == 0:
        reviews = None

    random_movies = services.get_random_movies(repo.repo_instance)
    for movie in random_movies:
        movie['hyperlink'] = url_for('movies_bp.brows_movies', rank = movie['Rank'])


    prev_movie_url = None
    next_movie_url = None
    total_movies = services.get_len_all_movies(repo.repo_instance)


    if (int(movie_rank) - 1 > 0):
        prev_movie_url = url_for('movies_bp.brows_movies', rank = (int(movie_rank) - 1))

    if (int(movie_rank) + 1 <= total_movies):
        next_movie_url = url_for('movies_bp.brows_movies', rank = (int(movie_rank) + 1))

    if 'username' in session:
        username = session['username']

        user_watch_list = services.get_watch_list(username, repo.repo_instance)

        current_movie = services.check_for_user_watch_list(current_movie, user_watch_list, repo.repo_instance)

    return render_template(
        'movies/reviews_on_movie.html',
        current_movie=current_movie,
        form=form,
        handler_url=url_for('movies_bp.make_review_for_movie'),
        prev_movie_url = prev_movie_url,
        next_movie_url = next_movie_url,
        reviews = reviews,
        random_movies = random_movies
    )




@movies_blueprint.route('/add_to_watchlist', methods=['GET', 'POST'])
@login_required
def add_to_watchlist():

    username = session['username']
    movie_rank = request.args.get('rank')

    movie = services.get_movie_object(int(movie_rank), repo.repo_instance)

    user_watchlist = services.get_watch_list(username, repo.repo_instance)


    if movie not in user_watchlist:
        user_watch_list = services.add_to_watchlist(username, movie, repo.repo_instance)
    else:
        user_watch_list = services.remove_movie_from_watchlist(int(movie_rank), username, repo.repo_instance)

    current_movie = services.get_movie(int(movie_rank), repo.repo_instance)
    current_movie = services.check_for_user_watch_list(current_movie, user_watch_list, repo.repo_instance)

    total_movies = services.get_len_all_movies(repo.repo_instance)

    random_movies = services.get_random_movies(repo.repo_instance)

    for movie in random_movies:
        movie['hyperlink'] = url_for('movies_bp.brows_movies', rank = movie['Rank'])

    prev_movie_url = None
    next_movie_url = None

    if (int(movie_rank) - 1 > 0):
        prev_movie_url = url_for('movies_bp.brows_movies', rank = (int(movie_rank) - 1))

    if (int(movie_rank) + 1 <= total_movies):
        next_movie_url = url_for('movies_bp.brows_movies', rank = (int(movie_rank) + 1))


    current_movie['add_review_url'] = url_for('movies_bp.make_review_for_movie', rank = current_movie['Rank'])

    reviews = services.get_movie_reviews(int(movie_rank), repo.repo_instance)
    if len(reviews) == 0:
        reviews = None

    return render_template(
        'movies/movies.html',
        title='Movies',
        current_movie = current_movie,
        random_movies = random_movies,
        prev_movie_url = prev_movie_url,
        next_movie_url = next_movie_url,
        reviews = reviews
    )





class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    valid_input = []
    input = 1.0
    while input <= 10:
        valid_input.append(round(input, 2))
        input += 0.01
    rating = FloatField('Rating', [
        DataRequired(message='You must enter float number between 1.00 and 10.00'),
        InputRequired(message = 'You must enter float number between 1.00 and 10.00'),
        AnyOf(valid_input, message = 'You must enter float number between 1.00 and 10.00')])


    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your comment must not contain profanity')])

    movie_rank = HiddenField("Movie Rank")
    submit = SubmitField('Post')


