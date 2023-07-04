import tornado.ioloop
import tornado.web
import tornado.autoreload

class InterfaceHandler(tornado.web.RequestHandler):
    '''Response handler for HTTP requests to the webpage/UI'''
    def get(self):
        '''GET: Display webpage'''
        self.render("index.html")

class APIHandler(tornado.web.RequestHandler):
    '''Response Handler for HTTP requests to the API'''

    def get(self):
        '''GET: Handle CREATE/UPDATE operation'''
        self.write("get req")
    
    def post(self):
        '''POST: Handle READ operation'''
        received_data = self.request.body  # Get the request body data
        # Process the received data
        response_data = {'message': 'Bye, Torando!1'}
        self.write(response_data)
        self.write(received_data)
        self.write("Bye, Tornado!2")

    def delete(self):
        '''DELETE: Handle DELETE operation'''
        pass


def create_app():
    '''App Handler Creator'''
    return tornado.web.Application([
        (r'/', InterfaceHandler),
        (r'/guid/', APIHandler)
    ], template_path="templates")

if __name__ == "__main__":
    app = create_app()
    app.listen(8888)
    tornado.autoreload.start()  # Enable autoreload
    tornado.ioloop.IOLoop.current().start()