from sqlalchemy import Column,String,Integer
from resume_builder import db

class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,autoincrement=True)
    first_name = Column(String,nullable=False)
    last_name = Column(String,nullable=False)
    email = Column(String,unique=True)
    hash = Column(String,nullable=False)