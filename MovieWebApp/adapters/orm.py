from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey, Float
)
from sqlalchemy.orm import mapper, relationship

from MovieWebApp.domain import model

metadata = MetaData()


users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)


movies = Table(
    'movies', metadata,
    Column('rank', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('description', String(1024), nullable=False),
    Column('director_id', ForeignKey('directors.id')),
    Column('release_year', Integer, nullable=False),
    Column('runtime_minutes', Integer, nullable=False),
    Column('rating', Float, nullable=False),
    Column('revenue', Float, nullable=False)
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('movie_rank', ForeignKey('movies.rank')),
    Column('review_text', String(1024), nullable=False),
    Column('rating', Float, nullable=False),
    Column('timestamp', String, nullable=False)
)


actors = Table(
    'actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(100))
)


actors_names = Table(
    'actors_names', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('actor_id', ForeignKey('actors.id')),
    Column('movie_rank', ForeignKey('movies.rank'))
)

genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False)
)

genres_names = Table(
    'genres_names', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('genre_id', ForeignKey('genres.id')),
    Column('movie_rank', ForeignKey('movies.rank')),
)

directors = Table(
    'directors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(100), nullable=False)
)

watch_lists = Table(
    'watch_lists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('movie_rank', ForeignKey('movies.rank'))
)

def map_model_to_tables():

    movie_mapper = mapper(model.Movie, movies, properties={
        'rank': movies.c.rank,
        'title': movies.c.title,
        'genres': relationship(model.Genre, secondary = genres_names),
        'release_year': movies.c.release_year,
        'description': movies.c.description,
        'actors': relationship(model.Actor, secondary = actors_names),
        'runtime_minutes': movies.c.runtime_minutes,
        'rating': movies.c.rating,
        'revenue': movies.c.revenue,
        'director': relationship(model.Director)
    })


    mp = mapper(model.Review, reviews, properties={
        'rating': reviews.c.rating,
        'movie': relationship(model.Movie),
        'review_text': reviews.c.review_text,
        'timestamp': reviews.c.timestamp
    })

    mapper(model.User, users, properties={
        'user_name': users.c.username,
        'password': users.c.password,
        'watch_list': relationship(model.User, secondary = watch_lists),
        'reviews': relationship(model.Review)
    })

    mapper(model.Actor, actors, properties={
        '_actor_full_name': actors.c.name
    })

    mapper(model.Genre, genres, properties={
        '_genre_name': genres.c.name
    })

    mapper(model.Director, directors, properties={
        '_director_full_name': directors.c.name
    })

