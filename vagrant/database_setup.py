import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String #classes import from SQLAlchemy for mapper code
from sqlalchemy.ext.declarative import declarative_base #used in the configuration and class code
from sqlalchemy.orm import relationship #to create foreign key relationships
from sqlalchemy import create_engine #used in configuration code


Base = declarative_base() #lets SQLAlchemy know that classes are special SQLAlchemy classes that correspond to tables in db

class Restaurant(Base):
	__tablename__ = 'restaurant'
	
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)

class MenuItem(Base):
	__tablename__ = 'menu_item' 
	
	name =Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	description = Column(String(250))
	price = Column(String(8))
	course = Column(String(250))
	restaurant_id = Column(Integer,ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)

	# Defines and formats what data to send across
	@property
	def serialize(self):
		#Returns obj data in easily serializeable format
		return {
			'name': self.name,
			'description': self.description,
			'id': self.id,
			'price': self.price,
			'course': self.course,
		}


# at end of file #
engine = create_engine('sqlite:///restaurantmenu.db') #points to db being used
#create_engine creates a new file that can be used similarly to a more robust db like MySQL or PostgreSQL
Base.metadata.create_all(engine)#takes classes & adds them as new tables in db
