# this is not the complete models.py, but enough to see the differences
from tornado_sqlalchemy import declarative_base

Base = declarative_base

class Task(Base):
    # and so on, because literally everything's the same...


##### como criar modelo (igual slqalchemy normal)
 from sqlalchemy import Column, BigInteger, String
 from tornado_sqlalchemy import declarative_base

 DeclarativeBase = declarative_base()

 class User(DeclarativeBase):
     id = Column(BigInteger, primary_key=True)
     username = Column(String(255), unique=True)

