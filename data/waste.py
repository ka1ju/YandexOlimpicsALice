import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Waste(SqlAlchemyBase):
    __tablename__ = 'waste'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    account_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.String, default=str(datetime.datetime.now().strftime("%d.%m.%Y")))
    category = sqlalchemy.Column(sqlalchemy.String, nullable=True)