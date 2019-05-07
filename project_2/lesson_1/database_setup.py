import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
   __tablename__ = 'restaurant' # Creates a table called restaurant. 

   name = Column(String(80), nullable=False) # Creating column called name. 
   # name of the restaurant is 80 characters long. 
   # Cannot create a new entry in the table if the restuarant name is left empty. 


   id = Column(Integer, primary_key=True) # Creating a column called id (primary key).
   # data type = Integer. 
   # Creates this as a primary key to the table.



class MenuItem(Base):
   __tablename__ = 'menu_item'
   
   #  Creating columns in menu_item table.
   name = Column(String(80), nullable=False)

   id = Column(Integer, primary_key=True)

   course = Column(String(250))

   description = Column(String(250))

   price = Column(String(8))

   restuarant_id = Column(Integer, ForeignKey('restaurant.id'))

   restaurant = relationship(Restaurant) # This shows the relationship between our restaurant table class.




engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
