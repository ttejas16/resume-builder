import os
import google.generativeai as genai
import jwt
from dotenv import load_dotenv
from flask import Flask,request,make_response,jsonify
from flask_cors import CORS, cross_origin
from sqlalchemy import Table,Column,Integer,String
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import engine
from werkzeug.security import generate_password_hash,check_password_hash


load_dotenv()


GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')


genai.configure(api_key=GOOGLE_API_KEY)


db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = engine.URL.create('postgresql+psycopg2',DB_USER,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)


db.init_app(app)
CORS(app,supports_credentials = True);


class Users(db.Model):
    email = Column(String,primary_key=True)
    uhash = Column(String)


with app.app_context():
    db.create_all()


@app.route("/resume/learn/<prompt>", methods = ["GET"])
def get_resume_data(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt);
    
    print(response.text)
    return ["some thing changed"]


def generate_token(email):
    key  = "secret"
    token = jwt.encode(payload = { "email":email }, key = key)
    return token


@app.post("/auth/login")
def login():
    email:str = request.json.get('email', None)
    password:str = request.json.get('password', None)

    print(email,password,request.json)

    if (not email) or (not password):
        return { "success":False , "msg":"empty credentials are not valid" }, 401
    
    email = email.strip()
    password = password.strip()

    res = db.session.execute(db.select(Users).where(Users.email == email)).scalars().all()

    if (not (len(res) > 0)) or (not check_password_hash(res[0].uhash, password)):
        return { "success":False , "msg":"please enter valid credentials" }, 401
    
    # generate JWT token and add it to cookies
    token = generate_token(email)
    resp = make_response({ "success":True , "msg":"successful log in" }, 200)
    resp.set_cookie(key = 'token',value = token,domain="127.0.0.1:5500")

    return resp



@app.post("/auth/signup")
def signup():
    email:str = request.json.get('email', None)
    password:str = request.json.get('password', None)

    if (not email) or (not password):
        return { "success":False , "msg":"empty credentials are not allowed" }, 401

    email = email.strip()
    password = password.strip()

    res = db.session.execute(db.select(Users).where(Users.email == email)).scalars().all()

    if len(res) > 0:
        return { "success":False , "msg":"email already registered" }, 409

    phash = generate_password_hash(password, salt_length = 10)
    new_user = Users(email = email, uhash = phash)

    db.session.add(new_user)
    db.session.commit()

    return { "success":True , "msg":"successfully registered" }, 200
    

    


if __name__ == "__main__":
    app.run(debug=True)