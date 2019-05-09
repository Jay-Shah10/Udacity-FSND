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
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                #Printing the output.
                output = ''
                output += "<html><body>"
                for restaurant in restaurants:
                    output += restaurant.name + "</br>"
                    # output += "</br>"
                    output += "<a href='#'> Edit </a></br>"
                    output += "<a href='#'> Delete</a></br>"
                    output += "</br>"

                output += "</body></html>"
                self.wfile.write(output)
                return 

            if self.path.endswith("/hello"): # if the url ends with /hello do the following.
                self.send_response(200) # sends a response 200 for success.
                self.send_header('Content-type', 'text/html') # returns some headers.
                self.end_headers()

                output = "" # what kind of output.
                output += "<html><body>"

                output +="Hello!" # what we will show.
                
                output += """<form method='POST' enctype='multipart/form-data' action='/hello'>
                             <h2>What would you like me to say?</h2>
                             <input name="message" type="text">
                             <input type="submit" value="Submit">
                             </form>"""
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
                
                output += """<form method='POST' enctype='multipart/form-data' action='/hello'>
                              <h2>What would you like me to say?</h2>
                             <input name="message" type="text">
                             <input type="submit" value="Submit">
                             </form>"""

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
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output = ""
            output += "<html><body>"
            output += "<h2> Okay, how about this: </h2"
            output += "<h1> %s </h1>" % messagecontent[0]

            output += """<form method='POST' enctype='multipart/form-data' action='/hello'>
                         <h2>What would you like me to say?</h2>
                        <input name="message" type="text">
                        <input type="submit" value="Submit">
                        </form>"""
            output += "</body></html>"
            self.wfile.write(output)
            print output

        except IOError: 
            self.send_error(404,"Not Found %s" % self.path)
            

def main():
    try: 
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print "Web server running on port %s" %port
        server.serve_forever()


    except KeyboardInterrupt as interruption:
        print "Stopping web server."
        server.socket.close()


if __name__ == "__main__":
    main()