# import Flask class from Flask library
from flask import Flask, render_template, url_for
# for db CRUD ops
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
# create instance of Flask class with name of running app
app = Flask(__name__)

#connect to db
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# @ wraps func inside the app.route func that Flask has already created
# calls func that follows whenever server receives request with matching URL
@app.route('/restaurants/<int:restaurant_id>/')
# if the above routes are sent from browser, below func code is executed
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
	# return rendered template
	return render_template('menu.html', restaurant=restaurant, items=items)
	
# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
	return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
	return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
	return "page to delete a menu item. Task 3 complete!"

# if statement ensures that server only runs if script is run directly
#	from Python interpreter & not used as an imported module
if __name__ == '__main__':
	# in debug mode, user of app can execute arbitrary Python code on comp
	app.debug = True
	# run func runs local server with app
	# by default, server is only accessible from the host machine & not 
	#	any other computer 
	app.run(host = '0.0.0.0', port = 5000)