import datetime
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

from .db_session import SqlAlchemyBase
from sqlalchemy import orm

class User(SqlAlchemyBase):
     __tablename__ = 'users'

     name = sa.Column(sa.String, primary_key=True, unique=True, nullable=True)
     #about = sa.Column(sa.String, nullable=True)
     email = sa.Column(sa.String, index=True, unique=True, nullable=True)
     hashed_password = sa.Column(sa.String, nullable=True)
     created_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
     message = orm.relation("Message", back_populates='user')


     def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

     def check_password(self, password):
        return check_password_hash(self.hashed_password, password)