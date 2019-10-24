# Sua primeira API assíncrona!

## Olá galera da Python Brasil 2019!

Sejam muito bem vindos ao tutorial de APIs Assíncronas, feito pelo [Genilson](https://github.com/jgdsfilho) e [Tyrone](https://github.com/tyronedamasceno).


### Inicialmente, vamos montar nosso ambiente!

Aqui utilizaremos Python 3.6.x e mongoDB,  sugerimos fortemente que usem um ambiente virtual isolado (explicaremos como fazer).

#### Criando o ambiente virtual:

-  Para os usuários de Linux (debian-based), simplismente executar:

`$ sudo apt install virtualenv`  OU  `$ sudo apt install python3-venv`  OU  `$ pip install virtualenv`

-  Com o virtualenv instalado, criaremos um ambiente virtual

`$ cd ~/`

`$ virtualenv -p python3 tutorial_pybr` (para os que instalaram pelo pip ou o apt virtualenv)

OU

`$ python3 -m venv tutorial_pybr` (para quem instalou pelo apt python3-venv)

-  Agora que todos criamos o nosso virtualenv, precisamos ativá-lo.

`$ source ~/tutorial_pybr/bin/activate`

Feito isso, deve aparecer o nome do seu venv entre parênteses no shell, como na imagem abaixo:

![terminal-01](images/terminal-01.png)

-  Inicialmente, utilizaremos o [Tornado](https://tornadoweb.org/en/stable/) e o [Motor](https://motor.readthedocs.io/en/stable/index.html)  

`$ pip install tornado motor

#### Instalando o mongodb

Para instalar o mongo, sugerimos os tutoriais oficiais da documentação do MongoDB.

https://docs.mongodb.com/manual/installation/

ps: *A instalação para linux debian-based e mac são bem rápidas e simples. Acredito que em outros sistemas/distros devem ser também, mas qualquer coisa dá um grito que a gente desenrola =D*

### Agora que já temos o venv pronto e o mongo instalado, vamos pra um pouco de teoria (bem pouco)

-  Inicialmente, o que é uma API?

Uma API (*application programming interface*) é uma forma de abrir o seu sistema para terceiros, sem que estes tenham acesso direto ao seu código, seu banco, além de que você pode controlar o que e como eles terão acesso.

Por exemplo, em uma suposta API de um banco, um usuário pode acessar sua conta e verificar seu saldo, mas não pode acessar a conta do coleguinha. Além disso, mesmo ele podendo acessar sua conta e ver seu saldo, ele não pode (ou pelo menos não deveria) conseguir alterar de maneira descontrolada o seu saldo.

Dúvidas? Fiquem a vontade para perguntar!

- Tá, mas e esse Tornado, qual a diferença dele para o flask, por exemplo?

Bem, o tornado, assim como flask e diversos outros, é um framework web, que te permite iniciar um servidor para receber e tratar requisições. A principal diferença do tornado para a maioria dos outros, é que ele implementa nativamente um sistema de controle de requisições assíncronas, o que dá uma grande vantagem na hora de escalar essa aplicação.

- Assíncrono??

Isso! Geralmente, as aplicações são síncronas, isso quer dizer que uma próxima atividade só será realizada após a finalização da anterior. Quando trabalhamos de forma assíncrona, isso não precisa ocorrer, atividades que forem mais lentas, não irão bloquear nosso processamento enquanto não terminarem.

Um exemplo: Pensa numa pizzaria, quando você liga e pede uma pizza, eles não esperam até a sua ficar pronta para poder receber outro pedido. Eles vão recebendo os pedidos, e conforme eles ficam prontos são enviados, inclusive, não necessariamente na ordem em que foram pedidos, pois um pedido de 10 pizzas irá demorar mais que apenas uma.

Então a assincronia do Tornado é **QUASE** isso, quando recebemos uma requisição e sabemos que algo vai demorar, deixamos essa coisa acontecendo (requisição a um serviço externo, consulta a um banco de dados, assar uma pizza, etc...) e vamos recebendo mais requisições. Isso nos traz um ganho de performance.

### Então...

![show-me-the-code](images/show-me-the-code.jpg)

### Vamos lá!

-  Inicialmente, vamos criar uma pasta e nosso arquivo de hello world do Tornado.

```
$ mkdir ~/tutorial && cd ~/tutorial
$ touch hello_world.py
```

No arquivo `hello_world.py` vamos inserir o seguinte código (novamente, qualquer dúvida **PODEM PERGUNTAR**):
Além disso, os arquivos e códigos estão neste repositório.


```
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application


class MainHandler(RequestHandler):
    def get(self):
        self.write('E aí galera da Python Brasil 2019!')


if __name__=='__main__':
    app = Application([('/', MainHandler)])
    app.listen(8000)
    IOLoop.current().start()
```

Esse código é bem simples, e implementa um endpoint (que aceita somente o método http GET) na rota **"/"**.

Vamos testar? No terminal rode o comando `$ python hello_world.py`, ele deve iniciar e ficar em branco mesmo. Em seguida, no browser acesse `localhost:8000`, ou no terminal execute `$ curl localhost:8000`.

Em ambos você deve ver a mensagem que escrevemos no método get do código!

### Parabéns! Você fez sua primeira aplicação usando Tornado

EXEMPLO DO ASSÍNCRONO AQUI

### Vamos ao que interessa né!

Tudo muito bom, tudo muito bonito, mas você veio aqui pra FAZER UMA API, então, vamos fazer uma API!

O que será essa API que faremos aqui? Estamos na Python Brasil né my friend, além de todas as palestras, tutoriais, conversas no corredor, novas amizades, etc, etc etc... 

Uma das atividades muito importantes são os PyBar's! E nada mais justo, que uma aplicação que nos ajude a organizar todos os rolês que daremos por aqui né?! (*ouvi dizer que Ribeirão Preto tem mais cervejaria que gente*)

Bem, nosso sistema contemplará um total de 01(um) modelo! Será o:

**ROLÊ**, que possui os seguintes atributos:
-  nome
-  endereco
-  data
-  hora
-  preco_da_cerveja
-  tem_karaoke
-  quem_vai

E teremos o endpoint:

*/role*, que aceitará os métodos GET e POST.

No GET, traremos as informações de todos os rolês marcados, no POST poderemos criar um novo rolê (ou atualizar caso este já exista).

Antes de começar, inicialize um repositório local com o comando abaixo:

`$ git init`

Vamos começar com nosso arquivo base, será o `__init__.py`.

```
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler

from motor import motor_tornado


class MainHandler(RequestHandler):
    def get(self):
        self.write("Olá galera da Python Brasil 2019! "
                   "Para ver os rolês faça requisições para '/roles'")


def main():
    port = 8000

    client = motor_tornado.MotorClient('localhost', 27017)
    db = client.roles_db

    app = Application([
        ('/', MainHandler),
       ],
       db=db
    )

    http_server = HTTPServer(app)
    http_server.listen(port)
    print('Listening on http://localhost:%i' % port)
    IOLoop.current().start()


if __name__== '__main__':
    main()

```

A grande diferença deste para o arquivo que já haviamos criado antes no Hello World, é que agora estamos instanciando também o nosso banco mongo. Para isso, importamos o `motor` e instanciamos um objeto `MotorClient`. Depois, informamos ao Application que este será o DB que usaremos.


Em seguida, criaremos o nosso arquivo `views.py` onde faremos o nosso RequestHandler principal para tratar de fato dos rolês!

Nele, criaremos uma classe BaseView, para evitar duplicação de código futuramente =D.

```
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
        self.required_params = ('nome', )
        self.acceptable_params = (
            'hora', 'preco_da_cerveja', 'tem_karaoke', 'quem_vai', 'endereco',
            'data'
        )
        self.all_params = self.required_params + self.acceptable_params

    async def get(self):
        data = await self._do_find_all()
        self.write({
            'data': [self._format_result_to_dict(d) for d in data]
        })

    async def _do_find_all(self):
        cursor = self.db.find()
        all_data = [doc for doc in await cursor.to_list(length=1000)]
        return all_data

    def _format_result_to_dict(self, mongo_result):
        result_dict = {key: mongo_result.get(key) for key in self.all_params}
        return result_dict

```

Além da classe BaseView, criamos uma classe RolesHandler (no mesmo padrão que já haviamos criado antes) com um método GET. Esse método já está sendo tratado com `async` e `await` para que possamos ter requisições assíncronas.

Agora, precisamos importar este Handler e colocá-lo na definição de Handlers no `__init__.py`

```
from views import BaseView, RolesHandler

...

app = Application([
        ('/', MainHandler),
        ('/roles', RolesHandler),
       ],
       db=db
    )
```

Já podemos testar se as conexões com o banco estão funcionando!

Só fazer uma requisição `$ curl localhost:8000/roles`

Provavelmente você obteve um JSON vazio como resposta, então, precisamos adicionar valores ao nosso banco!

Para isso, precisamos criar o método POST no `views.py`

```
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
        }, status=201)

    async def _do_find(self, nome):
        cursor = self.db.find({'nome': nome})
        data = await cursor.to_list(length=1)
        return data

    async def _do_update_one(self, _id, data):
        await self.db.replace_one({'_id': _id}, data)

    async def _do_insert_one(self, data):
        await self.db.insert_one(data)

    def _validate_params(self, body):
        errors = []
        for param in self.required_params:
            if param not in body:
                errors.append({param: 'Required parameter'})
        for param in body:
            if param not in self.all_params:
                errors.append({param: 'Unexpected parameter'})

        return errors
```

Além do POST, adicionamos alguns métodos auxiliares para lidar com o banco, e fazer validação de parâmetros.

### Fazendo Deploy no Heroku
#### Instalção e cadastros
* É necessário criar a conta no heroku no link abaixo:
    - https://www.heroku.com/
* Depois instalar o heroku-cli:
    - https://devcenter.heroku.com/articles/heroku-cli
* Após instalar o cli do heroku é necessário logar:
    
    `$ heroku login`
* Tamném será necessário se cadastrar no site https://mlab.com/ para podermos criar uma sandbox com MongoDB

#### Criando app com heroku

    `$ heroku create pybr-tornado3 nome_do_app`
Lembrando que esse do nome do app é único, não pode existir duplicados no heroku

* Configurando variável de ambiente do mongo

`$ heroku config:set MONGO_URL=mongodb://uses:pass@endereco_do_mlab`

* Fazendo push do deploy para o heroku

`$ git push heroku master`
