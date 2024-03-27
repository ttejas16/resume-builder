import os
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import engine


load_dotenv()
print("hello world")

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB`_PORT')
APP_SECRET = os.getenv('APP_SECRET')
JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = os.getenv('ALGORITHM')


db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = engine.URL.create('postgresql+psycopg2',DB_USER,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)
app.secret_key = APP_SECRET

db.init_app(app)


import resume_builder.authentication
import resume_builder.home
import resume_builder.create_resume

with app.app_context():
    db.create_all()