from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    rank = Column(Integer)