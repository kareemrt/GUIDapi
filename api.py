# Name: Kareem T
# Date: 07/02/2023
# Modu: api.py
# Desc: Primary framework (Tornado) driving GUID REST-Api and corresponding web-interface
import tornado.ioloop
import tornado.web
import tornado.autoreload
import validation
import database

class APIHandler(tornado.web.RequestHandler):
    '''Response Handler for HTTP requests to the API endpoints'''

    def get(self, subpath):
        '''GET: Handle READ operation'''
        if not validation.is_32_bit_hex(subpath): # Check GUID (32 char hex) given
            self.set_status(400)
            self.write("Error! - Read Error: Invalid GUID format (must be 32 Hexadecimal Uppercase characters)!") 
            return
        if not database.find_guid(subpath): # Check GUID in database
            self.set_status(400)
            self.write("Error! - Read Error: Invalid GUID: Record does not exist in the database!")
            return
        doc = database.find_guid(subpath)
        if not doc: # Check GUID has been retrieved
            self.set_status(400)
            self.write("Error! - Read Error: Could not retrieve GUID record!")
            return
        self.set_status(200)
        formatted_record = {'guid': doc['guid'], 'expire': doc['expire'], 'user': doc['user']}
        self.write(str(formatted_record))
        return

    def post(self, subpath):
        '''POST: Handle CREATE/UPDATE operation'''

        received_data = self.request.body  # Get the request body data  

        # UPDATE (existing guid given)
        if subpath != '' and database.find_guid(subpath): 
            status = validation.can_update(received_data, subpath)
            if type(status) != str: # No validation error
                update = database.update_guid(status) # returns bool
                if update: 
                    record = database.find_guid(subpath)
                    formatted_record = {'guid': record['guid'], 'expire': record['expire'], 'user': record['user']}
                    self.set_status(200)
                    self.write(str(formatted_record))
                    return
                self.set_status(400)
                self.write('ERROR! - Update error: Could not update record')
                return
            self.set_status(400) # Error
            self.write(status)
            return
        
        # CREATE (no existing guid given)
        status = validation.can_create(received_data, subpath) 
        if type(status) != str:
            record = database.create_guid(status)
            self.set_status(200)
            self.write(str(record))
            return
        self.set_status(400)
        self.write(status)
        return

    def delete(self, subpath):
        '''DELETE: Handle DELETE operation'''
        if subpath != '' and database.find_guid(subpath): 
            result = database.delete_guid(subpath)
            if result: 
                self.set_status(200)
                return
            self.set_status(400)
            self.write(f'Error! - Delete Error: Could not delete record for {subpath}')
            return
        self.set_status(400)
        self.write(f'Error! - Delete Error: Could not retrieve record for specified GUID: {subpath}')
        return
    
class WebHandler(tornado.web.RequestHandler):
    '''Response handler for HTTP requests to the webpage/UI'''
    def get(self):
        '''GET: Display webpage'''
        self.render("index.html")

def create_app():
    '''App Handler Creator'''
    return tornado.web.Application([
        (r'/', WebHandler), # Main route handled via web-page
        tornado.web.URLSpec(r'/guid/(.*)', APIHandler) # API-routes
    ], template_path="templates")

if __name__ == "__main__":
    app = create_app()
    app.listen(8888)
    tornado.autoreload.start()  # Debug mode
    tornado.ioloop.IOLoop.current().start()