from sqlalchemy import Column,String
from resume_builder import db

class User(db.Model):
    email = Column(String,primary_key=True)
    uhash = Column(String)