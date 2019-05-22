#!/usr/bin/python2

import os, sys, json
import random
import string
import httplib2

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask import session as login_session

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

from database_setup import Genre, Movies, Base


app = Flask(__name__)

# Create a connection to the database.
# avoiding the check for same thread. Gave a lot of errors when user refreshes.
engine = create_engine('sqlite://moviegenre.db', connect_args={'check_same_thread':False}) # do not check for same thread.
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/genres/')
def showGenres():
    """
    This method will dispaly all movie genres. They will be clickable.
    once the user clicks on this, it will display another page and it will show the actual movies.
    """
    pass

# Edit Genres.
@app.route('/genres/<int:genre_id>/edit/')
def editGenre(genre_id):
    """
    This method is responsible for making edits to the genre name.
    You can edit a specific Genre.

    TODO: add in code to select a particular genre and edit it.
    """
    pass


# Delete Genre.
@app.route('/genres/<int:genre_id>/delete/')
def delteGenre(genre_id):
    """
    This method is responsible for deleting a particular Genre.
    The user will be asked for a confirmation before deleting.

    TODO: add in code.
    """


# add new Movie Genre.
@app.route('/genres/new/')
def newGenre():
    """
    User can creat a new Move Genere.
    The database will be updated and the list will be displayed on the homepage.
    """