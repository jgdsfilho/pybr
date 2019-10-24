from tornado.web import RequestHandler

class RolesHandler(RequestHandler):
    def get(self):
        self.write("Hello, world!")
