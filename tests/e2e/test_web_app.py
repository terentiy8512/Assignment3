import pytest

from flask import session


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid username and password.
    response = client.post(
        '/authentication/register',
        data={'username': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['username'] == 'thorke'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_brows_movies(client, auth):
    response = client.get('/brows_movies?rank=2')
    assert response.status_code == 200
    assert b'Prometheus' in response.data

def test_search_by_title(client):
    response = client.get('/search_for_movie?category=title&page=1&search_string=gua')
    assert response.status_code == 200
    assert b'Guardians of the Galaxy' in response.data


def test_search_by_genre(client):
    response = client.get('/search_for_movie?category=genre&page=1&search_string=action')
    assert response.status_code == 200
    assert b'Guardians of the Galaxy' in response.data

def test_search_by_actor(client):
    response = client.get('/search_for_movie?category=actor&page=1&search_string=vin')
    assert response.status_code == 200
    assert b'Guardians of the Galaxy' in response.data

def test_search_by_director(client):
    response = client.get('/search_for_movie?category=director&page=1&search_string=James')
    assert response.status_code == 200
    assert b'Guardians of the Galaxy' in response.data