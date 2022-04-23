import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Accounts(SqlAlchemyBase):
    __tablename__ = 'accounts'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    accounts = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    bank = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    currency = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)