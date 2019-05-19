#!/usr/bin/python2
import requests
from flask import Flask
from flask import render_template, redirect, url_for, request, flash, jsonify

# Adding in imports for out database.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response

app = Flask(__name__)

CLIENT_ID = json.loads(
        open('client_secrets.json', 'r').read()
)['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"

# Making a connection to out database.
engine = create_engine('sqlite:///restaurantmenuwithusers.db', connect_args={'check_same_thread':False}) # this part was added to stop different thread.id errors.
Base.metadata.bind = engine 

# Database session.
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create a anit-forgery token.
@app.route('/login')
def showLogin():
    """"Method to show login page and create a token."""
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
    for x in range(32))
    login_session['state'] = state

    return render_template("login.html", STATE=state)

# This method is for connecting via google+
# Google+ has been inactive since Dec 2018.
# @app.route('/gconnect', method=['POST'])
# def gconnect():

def createUser(login_session):
    """Creating a user. Helper function.
        
    Arguments:
    login_session {[type]} -- Flask's login session.
        
    Returns:
    Creates a new user in the database.
    """
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    """Helper funtion to get user's info.
       
    Arguments:
    user_id {[int]} -- user'id from database.
    """
    user = session.query(User).filter_by(id=user_id).one()
    return user

def getUserID(email):
    """Helper function to get User' id from the database.
        
    Arguments:
    email {[string]} -- user's email.
    """
    try:
       user = session.query(User).filter_by(email=email).one()
       return user.id
    except:
       return None


#Making an API EndPoint (GET request)
@app.route('/restaurant/<int:restaurant_id>/menu/json')
def restaurantMenuJSON(restaurant_id):
    """
    This method is used to create a josn object for the menu page.
    :restaurant_id: id from table restaurant.
    :return: json object
    """
        
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItem=[i.serialize for i in items])

# Make and API endpoint for specific menu item (GET Request)
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menuitem_id>/json')
def menuItemJson(restaurant_id, menuitem_id):
    """
    Method used to create an api endpoint for specific menu items.
    """
    items = session.query(MenuItem).filter_by(id=menuitem_id).one()
    return jsonify(MenuItem=items.serialize)

@app.route('/')
def restaurants():
    restaurant = session.query(Restaurant)
    return render_template('restaurants.html', restaurants=restaurant)


# routing for Flask.
@app.route('/')
@app.route('/restaurant/<int:restaurant_id>/') # specific path for specific restaurant.
def restaurantMenu(restaurant_id):
    """
    This method is a test method used to demonstarte how we can use routing and flask framework to display
    what we did manually in webserver.py.

    :restaurant_id: restaurant id from database_setup.py.
    """
    # pull back information on our restaurants one at a time.
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template('menu.html', restaurant=restaurant, item=items, restaurant_id=restaurant_id)


    # printing out the restaurant name and menu items.
    # output = ''
    # output += '<h2>%s</h2>' % restaurant.name
    # # querying for menuItems per restaurant.
    # items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    # for item in items:
    #     output += item.name
    #     output += '</br>'
    #     output += item.description
    #     output += '</br>'
    #     output += item.price
    #     output += '</br>'
    #     output += '</br>'
    # return output

@app.route("/restaurant/<int:restaurant_id>/new/", methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    """
    If the user wants to add a new menu item.
    They can use the form that is created with templating.
    This method will handle post and get.
    if it is a post (add soemthing new) then it will extract name from request form and add to db.
    if it is not - then it will simply render the page for new menu item page.

    :restaurant_id: id from table Restaurant.
    """
    restaurant_name = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id, description=request.form['description'], price=request.form['price'])
        session.add(newItem)
        session.commit()
        flash("New Menu Item Created!") # this is a flash message, when the user adds a new menu item.
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id, restaurant=restaurant_name)


@app.route("/restaurant/<int:restaurant_id>/<int:menuitem_id>/edit/", methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menuitem_id):
    """
    Method usd to edit the name of a menu item.
    When the user clicks on the edit button, /templates/editmenuitem.html page is displayed.
    The use can choose to edit the name of the menuitem if they choose to, or they can press cancel 
    to be brought back to the menu page.

    :restaurant_id: id from table Restaurant.
    :menuitem_id: id from table MenuItem.
    """

    edited_menu_item = session.query(MenuItem).filter_by(id=menuitem_id).one()
    if request.method == 'POST':
        if request.form['name']:
            edited_menu_item.name = request.form['name']
            session.add(edited_menu_item)
            session.commit()
            flash("Menu Item has been edited.") # flashes the message when the user edits an item.
            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
            return render_template('editmenuitem.html', restaurant_id=restaurant_id, menuitem_id=menuitem_id, i=edited_menu_item)


@app.route("/restaurant/<int:restaurant_id>/<int:menuitem_id>/delete/", methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menuitem_id):
    """
    Method used to delete a menu item.
    When the use clicks on the delete button it will display /templates/deletemenuitems.html page.
    This page will dispaly a message to confirm the deletion.
    If the user does. Item should be deleted and redirected to the menu page.
    if the use chooses not to do so, they can press cancel.

    :restaurant_id = id from table Restaurant.
    :menuitem_id = id from table MenuItem.
    """
    delete_menu_item = session.query(MenuItem).filter_by(id=menuitem_id).one()
    if request.method == 'POST':
        session.delete(delete_menu_item)
        session.commit()
        flash("Menu Item has been deleted.") # This will be displayed when the user delets a menu item.
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

    else: 
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menuitem_id=menuitem_id, i=delete_menu_item)

    
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
