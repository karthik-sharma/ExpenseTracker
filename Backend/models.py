from sqlalchemy import Column, String, Integer, DateTime
from db_connection import Base
from db_connection import engine


class User(Base):
    __tablename__ = "users" 

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False) 
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)


class ExpenseInfo(Base):  
    __tablename__ = "expenses"

    username = Column(String, primary_key=True)  
    amount = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)

Base.metadata.create_all(engine)

