import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Message(SqlAlchemyBase):
    __tablename__ = 'messages'

    def __repr__(self):
        return f"<Message> {self.id} {self.title} {self.content}"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    #user_to_name = sqlalchemy.Column(sqlalchemy.Integer,
                                   #sqlalchemy.ForeignKey("users.name"), index=True, nullable=False)
    #user_from_id = sqlalchemy.Column(sqlalchemy.Integer,
                                #sqlalchemy.ForeignKey("users.id"), index=True, nullable=False)
    #user_to_id = sqlalchemy.Column(sqlalchemy.Integer,
                                #sqlalchemy.ForeignKey("users.id"), index=True, nullable=False)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    user_name = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("users.name"), index=True, nullable=False)
    user_to_name = sqlalchemy.Column(sqlalchemy.Integer,
                                index=True, nullable=False)
    #is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    user = orm.relation('User')

