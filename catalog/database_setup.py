import os, sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Genre(Base):
    """
    This is different movie genres.
    Genre name - this will be a column.
    id - primary key.

    TODO: Add relationship to User.
    """
    __tablename__ = 'genre'

    name = Column(String(250), nullable=False) # Genre name on table.

    id = Column(Integer, primary_key=True) # primary key for the genre table.


class Movies(Base):
    """
    Add in movies for particular genres.

    id - primary key for the movies.
    name - name of the movie.
    description - movie description.
    genre_id = ForeignKey to Genre.
    Relationship to Genre.

    TODO: User relationship and userid.
    """
    __tablename__ = 'movies'

    id = Column(Integer, primary_key= True) # primary key for movies table.

    name = Column(String(250), nullable=False) # name of the movie.

    description = Column(String(250), nullable=False) # description of the movie.

    genre_id = Column(Integer, ForeignKey('genre.id')) # foreign key to the genre table. Have to use '.id'

    genre = relationship(Genre) # shows the relationship to Genre table.


engine = create_engine("sqlite:///moviegenre.db")
Base.metadata.create_all(engine)