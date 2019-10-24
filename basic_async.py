import json
from random import randint
from time import sleep

from tornado.gen import coroutine
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application


def pseudo_slow_func():
    x = randint(1, 5)
    sleep(x)
    return {'waiting': x}


class BaseView(RequestHandler):
    """Base view for this application."""

    def prepare(self):
        self.form_data = {
            key: [val.decode('utf8') for val in val_list]
            for key, val_list in self.request.arguments.items()
        }

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    def send_response(self, data, status=200):
        """Construct and send a JSON response with appropriate status code."""
        self.set_status(status)
        self.write(json.dumps(data))


class SyncHandler(BaseView):
    def get(self):
        response = pseudo_slow_func()
        self.send_response(response)


class AsyncHandler(BaseView):
    @coroutine
    def get(self):
        response = pseudo_slow_func()
        if response:
            self.send_response(response)


if __name__=='__main__':
    app = Application([('/async', AsyncHandler), ('/sync', SyncHandler)])
    app.listen(8000)
    IOLoop.current().start()
