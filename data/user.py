from sqlalchemy import orm

from .db_session import SqlAlchemyBase
import sqlalchemy
import datetime


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column()
    nick = sqlalchemy.Column()
    difficult = sqlalchemy.Column()
    processing = sqlalchemy.Column()
    score = sqlalchemy.Column()
    ids_of_countries = sqlalchemy.Column(sqlalchemy.String)
