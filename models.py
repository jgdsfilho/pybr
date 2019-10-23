# this is not the complete models.py, but enough to see the differences
from sqlalchemy import Column, BigInteger, String, DateTime, Boolean
from tornado_sqlalchemy import declarative_base 

Base = declarative_base

class Roles(Base):
    __tablename__ = "roles"

    id = Column(BigInteger, primary_key=True)
    endereco = Column(String(300))
    data = Column(DateTime)
    preco = Column(String(5))
    karaoke = Column(Boolean, default=False)
    quem_vai = Column(String(50))
    # and so on, because literally everything's the same...


##### como criar modelo (igual slqalchemy normal)
#https://github.com/siddhantgoel/tornado-sqlalchemy/blob/master/examples/tornado_web.py -> mais exemplo
# from sqlalchemy import Column, BigInteger, String
# from tornado_sqlalchemy import declarative_base
#
# DeclarativeBase = declarative_base()
#
# class User(DeclarativeBase):
#     id = Column(BigInteger, primary_key=True)
#     username = Column(String(255), unique=True)
#
