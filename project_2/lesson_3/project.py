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
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

    else: 
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menuitem_id=menuitem_id, i=delete_menu_item)
    

    
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
