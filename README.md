# Sua primeira API assíncrona!

## Olá galera da Python Brasil 2019!

Sejam muito bem vindos ao tutorial de APIs Assíncronas, feito pelo [Genilson](https://github.com/jgdsfilho) e [Tyrone](https://github.com/tyronedamasceno).


### Inicialmente, vamos montar nosso ambiente!

Aqui utilizaremos Python 3.6.x e sugerimos fortemente que usem um ambiente virtual isolado (explicaremos como fazer).

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

-  Inicialmente, utilizaremos o [Tornado](https://tornadoweb.org/en/stable/) e o [Tornado-SQLAlchemy](https://tornado-sqlalchemy.readthedocs.io/en/latest/)  

`$ pip install tornado tornado-sqlalchemy`


### Agora que já temos o venv, vamos pra um pouco de teoria (bem pouco)

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

