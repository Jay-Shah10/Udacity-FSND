"""
This will have to main componentes. Handler and Main method.
This file acts as the websever to our webapp.
"""

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# Importing out need modules from restaurant databas.
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Connecting to the database.
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
    """
    Extends BaseHTTPRequestHandler class. 
    Uses method called do_GET() - what it will do when the request is GET.
    """
    def do_GET(self):
        """
        GET Method for the server.
        """
        try:
            
            if self.path.endswith("/restaurant"):
                # Gathering all resturant name from db.
                restaurants = session.query(Restaurant).all()
                output = ""
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                #Printing the output.
                output = ''
                output += "<html><body>"
                output += "<a href='/restaurant/new'> Make a new Restaurant.</a></br></br>"
                for restaurant in restaurants:
                    output += restaurant.name + "</br>"
                    output += "<a href='/restaurant/%s/edit'> Edit </a></br>" %restaurant.id
                    output += "<a href='/restaurant/%s/delete'> Delete</a></br>" % restaurant.id
                    output += "</br>"
                    output += "</body></html>"
                self.wfile.write(output)
                return 
            

            if self.path.endswith("/edit"):
                # Actions on what happens when you press the edit link.
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output +="<h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += """<form method='POST' enctype='multipart/form-data action='/restaurant/%s/edit>""" % restaurantIDPath
                    output += """<input name='newRestaurantName' type='text' placeholder ='%s'> """ % myRestaurantQuery.name
                    output += """<input type='submit' value='Rename'> """
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)


            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1> Are you sure you want to delete %s?" %myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/delete'> " %restaurantIDPath
                    output += "<input type='submit' value='Delete'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)




            if self.path.endswith("/restaurant/new"): # URL for adding a new restaurant.
                self.send_response(200) # sending a response code back.
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html></body>"
                output += "<h1>Make a new Restaurnt </h1>"
                # Creating a form that will take in data. Held in variable called 'newRestaurantName'
                output +="<form method='POST' enctype='multipart/form-data' action='/restaurant/new'>"
                output += """<input name="newRestaurantName" type="text" placeholder='New Restaurant Name'>"""
                output += """<input type='submit' value='Create'> """
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output)
                


            if self.path.endswith("/hello"): # if the url ends with /hello do the following.
                self.send_response(200) # sends a response 200 for success.
                self.send_header('Content-type', 'text/html') # returns some headers.
                self.end_headers()

                output = "" # what kind of output.
                output += "<html><body>"
                output +="Hello!" # what we will show.
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
                output += "<h2> What would you like me to say?</h2>"
                output += """<input name="message" type="text"> """
                output += "<input type='submit' value='Submit'>"
                output += "</form>"
                output += "</body></html>"

                self.wfile.write(output) # helps with debugging.
                print output # prints the output. 




            if self.path.endswith("/hola"): # if the url ends with /hello do the following.
                self.send_response(200) # sends a response 200 for success.
                self.send_header('Content-type', 'text/html') # returns some headers.
                self.end_headers()

                output = "" # what kind of output.
                output += "<html><body>"
                output += " &#161 Hola!" # what we will show.

                output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
                output += "<h2> What would you like me to say?</h2>"
                output += "<input name='message' type='text'>"
                output += "<input type='submit' value='Submit'>"
                output += "</form>"
                output += "</body></html>"
                
                
                self.wfile.write(output) # helps with debugging.
                print output # prints the output. 
                return
    
        except IOError:
            self.send_error(404, "File Not Found %s" %self.path)  # Used to handle errors.



    def do_POST(self):
        """
        Over writes the post method from http base module. 
        """
        try:

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery.name)
                        session.commit()

                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurant')
                        self.end_headers()
            
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurant')
                    self.end_headers()
                       


            # we are making sure that the url is in the correct path.
            if self.path.endswith("/restaurant/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type')) # extracting the headers.
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName') # gathering user input from variable called newRestaurantName.

                # Create a new Restaurant. 
                newRestaurant = Restaurant(name=messagecontent[0]) # user input.
                session.add(newRestaurant) # adding user input into the table.
                session.commit() # updated the table.

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurant') # Redirects to the restaurant page.
                self.end_headers()
                


            # self.send_response(301)
            # self.send_header('Content-type', 'text/html')
            # self.end_headers()
            # ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            # if ctype == 'multipart/form-data':
            #     fields = cgi.parse_multipart(self.rfile, pdict)
            #     messagecontent = fields.get('message')

            # output = ""
            # output += "<html><body>"
            # output += "<h2> Okay, how about this: </h2"
            # output += "<h1> %s </h1>" % messagecontent[0]

            # output += """<form method='POST' enctype='multipart/form-data' action='/hello'>
            #              <h2>What would you like me to say?</h2>
            #             <input name="message" type="text">
            #             <input type="submit" value="Submit">
            #             </form>"""
            # output += "</body></html>"
            # self.wfile.write(output)

        except IOError: 
            self.send_error(404,"Not Found %s" % self.path)

def main():
    try: 
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print "Web server running on port %s" %port
        server.serve_forever()


    except KeyboardInterrupt:
        print "Stopping web server."
        server.socket.close()


if __name__ == "__main__":
    main()