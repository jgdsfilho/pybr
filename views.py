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
    def __init__(self, application, request):
        super( RolesHandler, self ).__init__(application, request)
        _db = self.settings['db']
        self.collection = 'role_collection'
        self.db = _db[self.collection]
        self.required_params = ('nome', 'endereco', 'data')
        self.acceptable_params = (
            'hora', 'preco_da_cerveja', 'tem_karaoke', 'quem_vai'
        )
        self.all_params = self.required_params + self.acceptable_params

    def get(self):
        self.write("Hello, world!")

    async def post(self):
        body = json.loads(self.request.body)
        errors = self._validate_params(body)

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
                for key in self.all_params
            }

            if quem_ja_ia and quem_mais_vai:
                new_data['quem_vai'] = f'{quem_ja_ia}, {quem_mais_vai}'

            await self._do_update_one(role.get('_id'), new_data)
            result = await self._do_find(new_data['nome'])

            self.send_response({
                'message': 'Role successfully updated',
                'data': self._format_result_to_dict(result[0])
            })
            return

        await self._do_insert_one(body)
        result = await self._do_find(body['nome'])
        self.send_response({
            'message': 'Role successfully inserted',
            'data': self._format_result_to_dict(result[0])
        })

    async def _do_find_all(self):
        cursor = self.db.find()
        all_data = [
            json.dumps(doc) for doc in await cursor.to_list(length=1)
        ]
        return(all_data)

    async def _do_find(self, nome):
        cursor = self.db.find({'nome': nome})
        data = await cursor.to_list(length=1)
        return data

    async def _do_update_one(self, _id, data):
        await self.db.replace_one({'_id': _id}, data)

    async def _do_insert_one(self, data):
        await self.db.insert_one(data)

    def _format_result_to_dict(self, mongo_result):
        result_dict = {key: mongo_result.get(key) for key in self.all_params}
        return result_dict

    def _validate_params(self, body):
        errors = []
        for param in self.required_params:
            if param not in body:
                errors.append({param: 'Required parameter'})
        for param in body:
            if param not in self.all_params:
                errors.append({param: 'Unexpected parameter'})

        return errors
