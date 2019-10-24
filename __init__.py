import json

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application, RequestHandler
import os

from motor import motor_tornado

from views import BaseView, RolesHandler

port = int(os.environ.get("PORT", 5000))

class MainHandler(BaseView):
    def get(self):
        self.write("Olá galera da Python Brasil 2019! "
                   "Para ver os rolês faça requisições para '/roles'")


def main():

    MONGO_URL = os.environ.get('MONGO_URL')
    if not MONGO_URL:
        MONGO_URL = "mongodb://localhost:27017/"

    client = motor_tornado.MotorClient('localhost', 27017)
    db = client.test_db

    app = Application([
        ('/', MainHandler),
        ('/roles', RolesHandler),
       ],
       db=db
    )

    http_server = HTTPServer(app)
    http_server.listen(port)
    print('Listening on http://localhost:%i' % port)
    IOLoop.current().start()


if __name__== '__main__':
    main()
