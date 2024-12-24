from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean, Sequence, ForeignKey

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence('user_id', metadata=Base.metadata), primary_key=True, autoincrement=True)
    login = Column(String)
    hash_password = Column(String)
    is_teacher = Column(Boolean)

class Sudject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, Sequence('subject_id', metadata=Base.metadata), primary_key=True, autoincrement=True)
    name = Column(String)

class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, Sequence('grade_id', metadata=Base.metadata), primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    grade = Column(Integer)
    date = Column(String)