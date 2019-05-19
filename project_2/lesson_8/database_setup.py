import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
   """Class used to create user object in the database.
   
   Arguments:
       Base {[type]} -- sqlalchmey library.
   """
   __tablename__='user' # Creating a table called user.

   id = Column(Integer, primary_key=True) # primary key for the User table.
   name = Column(String(250), nullable=False) # User's name. Needed, cannot be left blank.
   email = Column(String(250), nullable=False) # user's email. Needed, cannot be left blank.
   picture = Column(String(250)) # optional to add a picture of the user.



class Restaurant(Base):
   """"Class used to creat a table for Restaurant in the database."""
   
   
   __tablename__ = 'restaurant' # Creates a table called restaurant. 

   name = Column(String(80), nullable=False) # Creating column called name. 
   # name of the restaurant is 80 characters long. 
   # Cannot create a new entry in the table if the restuarant name is left empty. 


   id = Column(Integer, primary_key=True) # Creating a column called id (primary key).
   # data type = Integer. 
   # Creates this as a primary key to the table.

   user_id = Column(Integer, ForeignKey('user.id'))
   user = relationship(User)



class MenuItem(Base):
   """ Class used to create a table for menuitem in the db.
   
   Keyword arguments:
   Base -- part of sqlalchmey library.
   Return: Creates a table in the db.
   """
   
   __tablename__ = 'menu_item'
   
   #  Creating columns in menu_item table.
   name = Column(String(80), nullable=False)

   id = Column(Integer, primary_key=True)

   course = Column(String(250))

   description = Column(String(250))

   price = Column(String(8))

   restaurant_id = Column(Integer, ForeignKey('restaurant.id'))

   restaurant = relationship(Restaurant) # This shows the relationship between our restaurant table class.

   user_id = Column(Integer, ForeignKey('user.id')) # Adding a foreign Key to the Column.

   user = relationship(User) # relationship to the User table.

   # JSON creation.
   @property
   def serialize(self):
      return {
         'name':self.name, 
         'description': self.description,
         'id': self.id,
         'price':self.price,
         'course':self.course 
      }


   


engine = create_engine('sqlite:///restaurantmenuwithusers.db')
Base.metadata.create_all(engine)
