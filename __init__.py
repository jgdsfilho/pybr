from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application, RequestHandler

from views import RolesHandler

import os
from tornado_sqlalchemy import make_session_factory

define('port', default=8888, help='port to list on')


class MainHandler(RequestHandler):
    def get(self):
        """Handle a GET request for saying Hello World!."""
        self.write("Olá galera da Python Brasil 2019! "
                   "Para ver os rolês faça requisições para '/roles'")


def main():

    app = Application([
        ('/', MainHandler),
        ('/roles', RolesHandler),
       ],
    )

    http_server = HTTPServer(app)
    http_server.listen(options.port)
    print('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()


if __name__== '__main__':
    main()
