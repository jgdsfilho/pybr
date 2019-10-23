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



Inicialmente, utilizaremos o [Tornado](https://tornadoweb.org/en/stable/) e o [Tornado-SQLAlchemy](https://tornado-sqlalchemy.readthedocs.io/en/latest/)  
