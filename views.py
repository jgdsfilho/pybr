import json

from tornado.web import RequestHandler


class BaseView(RequestHandler):
    """Base view for this application."""

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    def send_response(self, data, status=200):
        """Construct and send a JSON response with appropriate status code."""
        self.set_status(status)
        self.write(json.dumps(data))



class RolesHandler(BaseView):
    def get(self):
        self.write("Hello, world!")

    def post(self):
        required_params = ('nome', 'endereco', 'data')
        acceptable_params = (
            'hora', 'preco_da_cerveja', 'tem_karaoke', 'quem_vai'
        )
        errors = []
        body = json.loads(self.request.body)
        for param in required_params:
            if param not in body:
                errors.append({param: 'Required parameter'})
        for param in body:
            if param not in required_params + acceptable_params:
                errors.append({param: 'Unexpected parameter'})
        if errors:
            self.send_response({'errors': errors}, status=400)
            return

        self._do_insert_one(body)
        self.send_response({'message': 'Role successfully inserted'})

    def _do_insert_one(self, data, collection='role_collection'):
        db = self.settings['db']
        result = db[collection].insert_one(data)
