from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Sequence

class Base(DeclarativeBase):
    pass

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, Sequence('news_id', metadata=Base.metadata), primary_key=True, autoincrement=True)
    title = Column(String)
    date = Column(String)
    description = Column(Text)
    author = Column(String)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, Sequence('tag_id', metadata=Base.metadata), primary_key=True, autoincrement=True)
    name = Column(String)

class News_Tags(Base):
    __tablename__ = "news_tags"
    id_news = Column(Integer, ForeignKey('news.id'), primary_key=True)
    id_tag = Column(Integer, ForeignKey('tags.id'), primary_key=True)