from sqlalchemy import Column,String,Integer
from resume_builder import db

class Resume(db.Model):
    __tablename__ = "resume"
    id = Column(Integer,primary_key=True,autoincrement=True)
    resume_created = Column(Integer,default=0)
    resume_downloaded = Column(Integer,default=0)