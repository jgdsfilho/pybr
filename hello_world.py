from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application


class MainHandler(RequestHandler):
    def get(self):
        self.write('E aí galera da Python Brasil 2019!')


if __name__=='__main__':
    app = Application([('/', MainHandler)])
    app.listen(8000)
    IOLoop.current().start()
