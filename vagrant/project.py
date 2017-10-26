# import Flask class from Flask library
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
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


# Making an API Endpoint (GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	return jsonify(MenuItem=[i.serialize for i in items])
	
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(
		restaurant_id=restaurant_id, id=menu_id).one()
	return jsonify(MenuItem=[item.serialize])

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

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name=request.form['name'], 
			restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		flash("new menu item created!")
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id=restaurant_id) 

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', 
	methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
			session.add(editedItem)
			session.commit()
			flash("Menu Item Edited!")
			return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('editmenuitem.html', 
			restaurant_id=restaurant_id, item=editedItem)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', 
	methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		session.delete(deletedItem)
		session.commit()
		flash("Menu Item Deleted!")
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('deletemenuitem.html', item=deletedItem)
		

# if statement ensures that server only runs if script is run directly
#	from Python interpreter & not used as an imported module
if __name__ == '__main__':
	# Flask uses secret key to create sessions for users 
	app.secret_key = 'super_secret_key'
	# in debug mode, user of app can execute arbitrary Python code on comp
	app.debug = True
	# run func runs local server with app
	# by default, server is only accessible from the host machine & not 
	#	any other computer 
	app.run(host = '0.0.0.0', port = 5000)