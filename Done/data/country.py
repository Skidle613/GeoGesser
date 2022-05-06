from sqlalchemy import orm

from .db_session import SqlAlchemyBase
import sqlalchemy


class Country(SqlAlchemyBase):
    __tablename__ = 'countries'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column()
    capital = sqlalchemy.Column()
    flag = sqlalchemy.Column()
    difficult = sqlalchemy.Column()
