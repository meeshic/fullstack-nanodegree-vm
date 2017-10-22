# import Flask class from Flask library
from flask import Flask
# create instance of Flask class with name of running app
app = Flask(__name__)

# @ wraps func inside the app.route func that Flask has already created
# calls func that follows whenever server receives request with matching URL
@app.route('/')
@app.route('/hello')
# if the above routes are sent from browser, below func code is executed
def HelloWorld():
	return "Hello World!"

# if statement ensures that server only runs if script is run directly
#	from Python interpreter & not used as an imported module
if __name__ == '__main__':
	# in debug mode, user of app can execute arbitrary Python code on comp
	app.debug = True
	# run func runs local server with app
	# by default, server is only accessible from the host machine & not 
	#	any other computer 
	app.run(host = '0.0.0.0', port = 5000)