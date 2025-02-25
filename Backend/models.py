from sqlalchemy import Column, String, Integer, DateTime
from db_connection import Base


class User(Base):
    __tableame__ = "users"

    id = Column("id", Integer, primary_key=True)
    username = Column("username", String, primary_key=True)
    name = Column("name", String, nullable=False)
    password = Column("password", String, nullable=False)

class ExpanseInfo(Base):
    __tablename__ = "expenses"

    id = Column("id", Integer, primary_key=True)
    username = Column("username", String, primary_key=True)
    amount = Column("amount", Integer)
    category = Column("category", String)
    date = Column("date", DateTime)




