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
    collection = 'role_collection'

    def get(self):
        self.write("Hello, world!")

    async def post(self):
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

        role = await self._do_find(body.get('nome'))

        if role:
            role = role[0]
            quem_ja_ia = role.get('quem_vai')
            quem_mais_vai = body.get('quem_vai')

            new_data = {
                key: body.get(key) or role.get(key)
                for key in required_params + acceptable_params
            }

            if quem_ja_ia and quem_mais_vai:
                new_data['quem_vai'] = f'{quem_ja_ia}, {quem_mais_vai}'

            result = await self._do_update_one(role.get('_id'), new_data)
            self.send_response('gluglu')
            return

        result = await self._do_insert_one(body)
        self.send_response({'message': 'Role successfully inserted'})

    async def _do_find(self, nome):
        db = self.settings['db']
        cursor = db[self.collection].find({'nome': nome})
        data = await cursor.to_list(length=1)
        return data

    async def _do_update_one(self, _id, data):
        db = self.settings['db']
        result = await db[self.collection].replace_one({'_id': _id}, data)
        return result

    async def _do_insert_one(self, data):
        db = self.settings['db']
        result = await db[self.collection].insert_one(data)
        return result
