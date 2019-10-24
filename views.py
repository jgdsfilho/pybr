from tornado.web import RequestHandler

class RolesHandler(RequestHandler):
    def get(self):
        db = self.settings['db']
        self.write("Hello, world!")
