#!/usr/bin/python2

import os, sys, json
import random
import string
import httplib2

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask import session as login_session
from flask import make_response
import random, string

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

from database_setup import User, Genre, Movies, Base


app = Flask(__name__)

# Create a connection to the database.
# avoiding the check for same thread. Gave a lot of errors when user refreshes.
engine = create_engine('sqlite:///moviegenre.db', connect_args={'check_same_thread':False}) # do not check for same thread.
Base.metadata.bind = engine

# binding a session.
DBSession = sessionmaker(bind=engine)
session = DBSession()

################# Login ########################
@app.route('/login')
def showLogin():
    """
        This will show a third party login in feature.
        in this case we are using facebook to login.
        For this method it will create a session token that can be used
        to verify that the session is for the current user.
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

    # https://www.mattbutton.com/2019/01/05/google-authentication-with-python-and-flask/ use this to sign in with google

################# facebook login ########################
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    """
        We are using a third party authentication provider to log in a user.
        in this case we are using facebook. User must have a facebook account.
    """
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid State Parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    # Exchanging short lived token to a long live token.
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_id']
    app_secrets = json.loads(open('fb_client_secrets.json','r').read())['web']['app_secrets']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_seceret=%s&fb_exchange_token=%s' %(app_id, app_secrets, access_token)
    # url = 'https://graph.facebook.com/oauth/access_token=%s'%access_token
    h = httplib2.Http()
    result = h.request(url, "GET")[1]
    # use token to get user info from API.
    userinfo_url = 'https://graph.facebook.com/v2.8/me?'
    # token = result.split(',')[0].split(":")[1].replace('"', '') # original.
    token = result.split("&")[0] # new.
    print 'token-- %s' %token
    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    print json.dumps(data, indent=2, sort_keys=True)

    login_session['provider'] = 'facebook'
    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['facebook_id'] = data['id']
    # print login_session

    # The token must be stored  in the login_session in order to properly signout.
    login_session['access_token'] = token

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '</h1>'
    flash("Now logged in as %s" % login_session['username'])
    return output


################# facebook disconnect ########################
@app.route("/fbdisconnect")
def fbdisconnect():
    """
    This will delete the access token from that was gathered from facebook.

    :return: homepage. showGenres()
    """
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, method='DELETE')
    # return "You have logged out."
    return redirect(url_for("showGenres")) # redirects the user to the home page.


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    """
    THis method is used to logout.
    Here we will call fbdisconnect to delete the access_token that is given to us
    from facebook.
    We are also deleting the values returned to use in login_session.
    such as facebook_id, username, email, user_id, and provider.

    : return: the homepage.
    """
    if 'provider' in login_session:
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
            del login_session['username']
            del login_session['email']
            del login_session['user_id']
            del login_session['provider']
            print login_session
        flash("You have successfully been logged out.")
        return redirect(url_for('showGenres'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showGenres'))


    

################# User helper functions ########################
def createUser(login_session):
    """
    Creates a user in the database if they do not exist.

    :return: user_id - the primary key.
    """
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

# Helper functions.
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


################# shows Genres ########################
@app.route('/genres/')
def showGenres():
    """
    This method will dispaly all movie genres. They will be clickable.
    once the user clicks on this, it will display another page and it will show the actual movies.
    """
    genre = session.query(Genre).order_by(asc(Genre.name))
    if 'username' not in login_session:
        return render_template('publicgenre.html', genres=genre)
    else:
        return render_template('genre.html', genres=genre)

################# Edit Genre. ########################
# Edit Genres.
@app.route('/genres/<int:genre_id>/edit/')
def editGenre(genre_id):
    """
    This method is responsible for making edits to the genre name.
    You can edit a specific Genre.
    """
    edit_genre = session.query(Genre).filter_by(id=genre_id).one()
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        if request.form['name']:
            edit_genre = request.form['name']
            session.add(edit_genre)
            session.commit()
            flash("Movie Genre has been Edited.")
            return redirect(url_for("showGenres"))
    else:
        return render_template('editgenre.html', genre=edit_genre)

################# Delete Genre. ########################
# Delete Genre.
@app.route('/genres/<int:genre_id>/delete/', methods=['GET', 'POST'])
def deleteGenre(genre_id):
    """
    This method is responsible for deleting a particular Genre.
    The user will be asked for a confirmation before deleting.
    """

    # Getting the proper genre needed to delete by genre id.
    delete_genre = session.query(Genre).filter_by(id=genre_id).first()
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    if request.method == 'POST': # this only happens if the method is post.
        session.delete(delete_genre)
        session.commit() # deleteing the Movie Genre.
        flash("you have successfully deleted the movie genre.") # prints out a message if anything has been modified.
        return redirect(url_for('showGenres', genre_id=genre_id)) # redirects to the main page.
    else:
        return render_template('delete.html', genre=delete_genre) # Displays the delete page.

################# add new Genre. ########################
# add new Movie Genre.
@app.route('/genres/new/', methods=['GET', 'POST'])
def newGenre():
    """
    User can creat a new Move Genere.
    The database will be updated and the list will be displayed on the homepage.
    """
    genre = Genre()
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    if request.method == "POST":
        if request.form['name']:
            new_genre = request.form['name']
            session.add(Genre(name=new_genre))
            session.commit()
            flash("You Have created a new Genre.")
            return redirect(url_for('showGenres'))
    else:
        return render_template('newgenre.html')
        

################# shows movies. ########################
@app.route('/genres/<int:genre_id>/movies/')
def showMovies(genre_id):
    """This will display movies based on genres.
       this is connected via genre id. this is acting as foreign key in the movies table.
    """
    genre = session.query(Genre).filter_by(id=genre_id).one()
    movie = session.query(Movies).filter_by(genre_id=genre.id).all()

    if 'username' not in login_session:
        return render_template('publicshowmovies.html', movies=movie, genre=genre)
    else:
        return render_template('showmovies.html', movies=movie, genre=genre)


################# Add new Movie ########################
@app.route('/genres/<int:genre_id>/newmovie/', methods=['GET','POST'])
def addNewMovie(genre_id):
    """
    This will add new movies to a genre.
    """
    genre = session.query(Genre).filter_by(id=genre_id).one()
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))

    if request.method == 'POST':
       new_movie = Movies(name=request.form['title'], 
                          description=request.form['description'],
                          year=request.form['date'], 
                          genre_id=genre_id)
       session.add(new_movie)
       session.commit()
       flash("New Movie added.")
       return redirect(url_for('showMovies', genre_id=genre_id))
    else:
       return render_template('newmovie.html', genre=genre)
       
################# Individualt Movie ########################
# Shows individual movie.
@app.route('/genres/<int:genre_id>/movies/<int:movie_id>/')
def movie(genre_id, movie_id):
    """
    This method is responsible for makeing edits to the
    movie title, description, and year.
    """
    genre = session.query(Genre).filter_by(id=genre_id).one()
    movie = session.query(Movies).filter_by(id=movie_id).one()
    
    if 'username' not in login_session:
        return render_template('publicmovie.html', movie=movie, genre=genre)
    else:
        return render_template('movie.html', movie=movie, genre=genre)

################# Edit Movie ########################
@app.route('/genres/<int:genre_id>/movies/<int:movie_id>/edit/', methods=['GET', 'POST'])
def editMovie(genre_id, movie_id):
    """
    Responsible for makeing edits to the selected movie. 
    Make edits to the name, year, and description.
    """
    genre = session.query(Genre).filter_by(id=genre_id).one()
    movie = session.query(Movies).filter_by(id=movie_id).one()
    
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        description = request.form['description']

        if request.form['title'] == "" and request.form['year'] == "":
            movie.description = description

        elif request.form['year'] == "" and request.form['description'] == "":
            movie.name = title

        elif request.form['description'] == "" and request.form['title'] == "":
            movie.year = year

        else:
            movie.name = title
            movie.year = year
            movie.description = description

        session.add(movie)
        session.commit()
        flash("You have edited a movie.")
        return redirect(url_for('showMovies', genre_id=genre_id))
    else:
        return render_template('editmovie.html', genre=genre, movie=movie)

################# Edit Movie ########################
@app.route('/genres/<int:genre_id>/movies/<int:movie_id>/delete/', methods=['GET','POST'])
def deleteMovie(genre_id, movie_id):
    """
    This is used to delete a movie in the list.
    The use will get a confirmation pormpt. if they do so, they will redirected to the 
    show movies page. Flash mesage will be displayed stating they have deleted a movie.
    """
    genre = session.query(Genre).filter_by(id=genre_id).one()
    movie = session.query(Movies).filter_by(id=movie_id).one()

    if 'username' not in login_session:
        return redirect(url_for('showLogin'))

    if request.method=="POST":
        session.delete(movie)
        session.commit()
        flash("You have deleted a movie.")
        return redirect(url_for('showMovies', genre_id=genre.id))
    else:
        return render_template('deletemovie.html', genre=genre, movie=movie)

################# JSON endpoints ########################
# json endpoint for all genre.
@app.route('/genres/json')
def genreJSON():
    """This will display genres in JSON form."""
    genre = session.query(Genre).all()
    return jsonify(genres=[g.serialize for g in genre])

# json endpoint for all movies in a given genre.
@app.route('/genres/<int:genre_id>/movies/json')
def movieJSON(genre_id):
    """ This will dispaly all movies in JSON form."""
    movie = session.query(Movies).filter_by(genre_id=genre_id)
    return jsonify(movies=[m.serialize for m in movie])

# json endpoint for all movies.
@app.route('/movies/json/')
def allMoviesJSON():
    """returns json object for all movies."""
    movies = session.query(Movies).all()
    return jsonify(movie = [m.serialize for m in movies])

# json endpoint for one movie.
@app.route('/genres/<int:genre_id>/movies/<int:movie_id>/json')
def oneMovie(genre_id, movie_id):
    """returns json object for a specific movie. """
    genre = session.query(Genre).filter_by(id=genre_id).one()
    movie = session.query(Movies).filter_by(id=movie_id).one()
    return jsonify(movie.serialize)



if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)