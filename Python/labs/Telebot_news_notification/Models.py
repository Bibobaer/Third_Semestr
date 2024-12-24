from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey

class Base(DeclarativeBase):
    pass

class News(Base):
    __tablename__ = "news"
    id = Column(Integer,Sequence('news_id', metadata=Base.metadata), primary_key=True, autoincrement=True)
    title = Column(String)
    date =  Column(String)
    link = Column(String)

class Full_News(Base):
    __tablename__ = "full_news"
    id = Column(Integer, Sequence('fn_id', metadata=Base.metadata), primary_key=True, autoincrement=True)
    name = Column(String)