import os
import json

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application, RequestHandler

from motor import motor_tornado

from views import BaseView, RolesHandler

class MainHandler(BaseView):
    def get(self):
        self.write("Olá galera da Python Brasil 2019! "
                   "Para ver os rolês faça requisições para '/roles'")


def main():
    MONGO_URL = os.environ.get('MONGO_URL')

    client = motor_tornado.MotorClient(MONGO_URL, retryWrites=False)
    db = client['pybr-roles']

    app = Application([
        ('/', MainHandler),
        ('/roles', RolesHandler),
       ],
       db=db
    )

    http_server = HTTPServer(app)
    http_server.listen(8000)
    IOLoop.current().start()


if __name__== '__main__':
    main()
