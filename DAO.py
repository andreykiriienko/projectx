from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import pymysql
from misc import generate_alphanum_random_string, token_expire_time, time
import config as c

pymysql.install_as_MySQLdb()

engine = create_engine(f'mysql+pymysql://{c.DB_USERNAME}:{c.DB_PASSWORD}@{c.DB_HOST}/{c.DB_NAME}', encoding='utf8')

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    role = Column(String(50), default='user')
    date_creation = Column(TIMESTAMP, default=time)
    authenticate = Column(BOOLEAN, default=False)


class Auth(Base):
    __tablename__ = 'Auth'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False, unique=True)
    token = Column(String(60), default=generate_alphanum_random_string(59))
    token_expire_date = Column(TIMESTAMP, default=token_expire_time)
    user = relationship('User')


Base.metadata.create_all(engine)
