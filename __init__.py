import json

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application, RequestHandler

from motor import motor_tornado

from views import BaseView, RolesHandler

define('port', default=8888, help='port to list on')


class MainHandler(BaseView):
    def get(self):
        self.write("Olá galera da Python Brasil 2019! "
                   "Para ver os rolês faça requisições para '/roles'")


def main():

    client = motor_tornado.MotorClient('localhost', 27017)
    db = client.test_db

    app = Application([
        ('/', MainHandler),
        ('/roles', RolesHandler),
       ],
       db=db
    )

    http_server = HTTPServer(app)
    http_server.listen(options.port)
    print('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()


if __name__== '__main__':
    main()
