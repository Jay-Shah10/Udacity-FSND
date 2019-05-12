#!/usr/bin/python2

from flask import Flask
app = Flask(__name__)

# Adding in imports for out database.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Making a connection to out database.
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine 

# Database session.
DBSession = sessionmaker(bind=engine)
session = DBSession()

# routing for Flask.
@app.route('/') # home path.
@app.route('/restaurant/<int:restaurant_id>/') # specific path for specific restaurant.
def HelloWorld(restaurant_id):
    """
    This method is a test method used to demonstarte how we can use routing and flask framework to display
    what we did manually in webserver.py.

    :restaurant_id: restaurant id from database_setup.py.
    """

    # pull back information on our restaurants one at a time.
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    # printing out the restaurant name and menu items.
    output = ''
    output += '<h2>%s</h2>' % restaurant.name
    # querying for menuItems per restaurant.
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    for item in items:
        output += item.name
        output += '</br>'
        output += item.description
        output += '</br>'
        output += item.price
        output += '</br>'
        output += '</br>'
    return output

    
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
