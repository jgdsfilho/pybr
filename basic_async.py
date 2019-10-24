import time
from tornado import gen, httpclient
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.log import app_log
from tornado.options import define, options, parse_command_line
from tornado.web import Application, RequestHandler, URLSpec


DEBUG = True
PORT = 8888
FACEBOOK_URL = "http://api.facebook.com/restserver.php?format=json&method=links.getStats&urls={0}"
external_api_url = FACEBOOK_URL.format("http://globo.com")


# Options
define("debug", default=DEBUG, help="Enable or disable debug", type=bool)
define("port", default=PORT, help="Run app on the given port", type=int)


def create_app():
    """
    Create instance of tornado.web.Application.
    """
    routes = [
        URLSpec(r'/async', MainHandlerAsync),
        URLSpec(r'/block', MainHandlerBlocking)
    ]
    return Application(routes, **options.as_dict())


class MainHandlerBlocking(RequestHandler):

    def get(self):
        req = httpclient.HTTPRequest(external_api_url, method='GET')
        # we could use something like requests or urllib here
        client = httpclient.HTTPClient()
        response = client.fetch(req)

        # do something with the response (response.body)
        self.finish("from block")


class MainHandlerAsync(RequestHandler):

    async def get(self):
        req = httpclient.HTTPRequest(external_api_url, method='GET')
        client = httpclient.AsyncHTTPClient()
        # don't let the yield call confuse you, it's just Tornado helpers to make
        # writing async code a bit easier. This is the same as doing
        # client.fetch(req, callback=_some_other_helper_function)
        for i in range(100):
            response = await client.fetch(req)
        ### do something with the response (response.body)
        self.finish("from asynchronous")


def main():
    """
    Run main loop.
    """
    parse_command_line()
    application = create_app()
    server = HTTPServer(application)
    server.listen(options['port'])
    app_log.info("Service is running at port {0}".format(options['port']))
    io_loop = IOLoop.current()
    io_loop.start()


if __name__ == '__main__':
    main()
else:
    application = create_app()
