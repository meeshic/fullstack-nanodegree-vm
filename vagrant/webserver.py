from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi 
# import CRUD operations from Lesson 1
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Handler class: how to HTTP requests sent to server based on request type 
# Main method: instantiate server & specify listening port

# Handler
class webServerHandler(BaseHTTPRequestHandler):
	
	
	def do_GET(self):
		try: 
		
			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				restaurants = session.query(Restaurant).all()
				for restaurant in restaurants:
					output += restaurant.name
					output += "</br>"
					output += "<a href = '/restaurants/%d/edit'>Edit</a></br>" % restaurant.id
					output += "<a href = 'restaurants/%d/delete'>Delete</a></br>" % restaurant.id
					output += "</br>"
				output += "</br>"
				output += "<a href = '/restaurants/new'>Make a New Restaurant Here!</a>"
				output += "</body></html>"
				self.wfile.write(output)
				return
			
			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>Make a New Restaurant</h1>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
				output += "<input name='newRestaurantName' type='text'>"
				output += "<input type='submit' value='Create'>"
				output += "</form></body></html>"
				self.wfile.write(output)
				return
				
				
			if self.path.endswith("/edit"):
				restaurantID = 	self.path.rsplit('/', 2)[-2]
				restaurant = session.query(Restaurant).filter_by(
					id=restaurantID).one()
				if restaurant != []:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output = ""
					output += "<html><body>"
					output += "<h1>%s</h1>" % restaurant.name
					output += "<form method='POST' enctype='multipart/form-data' action='%s'>" % self.path
					output += "<input name='editRestaurantName' type='text' placeholder='%s'>" % restaurant.name
					output += "<input type='submit' value='Rename'>"
					output += "</form></body></html>"
					self.wfile.write(output)
					return
			
			if self.path.endswith("/delete"):
				restaurantID = 	self.path.rsplit('/', 2)[-2]
				restaurant = session.query(Restaurant).filter_by(
					id=restaurantID).one()
				if restaurant != []:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output = ""
					output += "<html><body>"
					output += "<h1>Are you sure you want to delete %s?</h1>" % restaurant.name
					output += "<form method='POST' action='%s'>" % self.path
					output += "<input type='submit' name='deleteRestaurant' value='Delete'>"
					output += "</form></body></html>"
					self.wfile.write(output)
					return					
		
		
		except IOError:
			self.send_error(404, 'File Not Found: %s' % self.path)


	def do_POST(self):
		try:	
			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					#collect fields in form
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newRestaurantName')
				

					# add to db
					newRestaurant = Restaurant(name=messagecontent[0])
					session.add(newRestaurant)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					# URL redirection
					self.send_header('Location', '/restaurants')
					self.end_headers()		
			
			if self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					#collect fields in form
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('editRestaurantName')
					
					
					# update db if entry exists
					restaurantID = 	self.path.rsplit('/', 2)[-2]
					restaurant = session.query(Restaurant).filter_by(id=restaurantID).one()
					if restaurant != []:
						restaurant.name = messagecontent[0]
						session.add(restaurant)
						session.commit()
						
						self.send_response(301)
						self.send_header('Content-type', 'text/html')
						# URL redirection
						self.send_header('Location', '/restaurants')
						self.end_headers()		

			if self.path.endswith("/delete"):
				# delete entry in db if entry exists
				restaurantID = 	self.path.rsplit('/', 2)[-2]
				restaurant = session.query(Restaurant).filter_by(id=restaurantID).one()
				if restaurant != []:
					session.delete(restaurant)
					session.commit()
					
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					# URL redirection
					self.send_header('Location', '/restaurants')
					self.end_headers()						
				
		except:
			pass
def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webServerHandler)
		print "Web Server running on port %s" % port
		server.serve_forever()
	except KeyboardInterrupt:
		print " ^C entered, stopping web server...."
		server.socket.close()

if __name__ == '__main__':
    main()