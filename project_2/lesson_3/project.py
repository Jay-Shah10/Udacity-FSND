#!/usr/bin/python2

from flask import Flask
from flask import render_template, redirect, url_for, request
app = Flask(__name__)

# Adding in imports for out database.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Making a connection to out database.
engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread':False})
Base.metadata.bind = engine 

# Database session.
DBSession = sessionmaker(bind=engine)
session = DBSession()

# @app.route('/')
# def restaurantMenu(restaurant_id):
#     restaurant = session.query(Restaurant).first()
#     items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
#     return render_template('menuitem.html', restaurant=restaurant, item=items)


# routing for Flask.
@app.route('/restaurant/<int:restaurant_id>/') # specific path for specific restaurant.
def restaurantMenu(restaurant_id):
    """j
    This method is a test method used to demonstarte how we can use routing and flask framework to display
    what we did manually in webserver.py.

    :restaurant_id: restaurant id from database_setup.py.
    """
    # pull back information on our restaurants one at a time.
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template('menu.html', restaurant=restaurant, item=items)


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

@app.route("/restaurant/<int:restaurant_id>/new/")
def newMenuItem(restaurant_id):
    """
    If the user wants to add a new menu item.
    They can use the form that is created with templating.
    This method will handle post and get.
    if it is a post (add soemthing new) then it will extract name from request form and add to db.
    if it is not - then it will simply render the page for new menu item page.
    """
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


@app.route("/restaurant/<int:restaurant_id>/<int:menuitem_id>/edit/", methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menuitem_id):

    edited_menu_item = session.query(MenuItem).filter_by(id=menuitem_id).one()
    if request.method == 'POST':
        if request.form['name']:
            edited_menu_item.name = request.form['name']
            session.add(edited_menu_item)
            session.commit()
            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
            return render_template('editmenuitem.html', restaurant_id=restaurant_id, menuitem_id=menuitem_id, i=edited_menu_item)


@app.route("/restaurant/<int:restaurant_id>/<int:menuitem_id>/delete/")
def deleteMenuItem(restaurant_id, menuitem_id):
    return "Here to delete a menu item."

    
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
