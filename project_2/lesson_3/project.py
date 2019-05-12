#!/usr/bin/python2

from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine 

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/') # if this path is executed then our app runs.
@app.route('/restaurant/<int:restaurant_id>/') # if this is the path out app shows.
def HelloWorld(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    output = ''
    output += '<h2>%s</h2>' % restaurant.name
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
