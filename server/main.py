import os
import copy
import datetime

import jwt
import pdfkit
import google.generativeai as genai

from dotenv import load_dotenv
from functools import wraps
from bs4 import BeautifulSoup

from sqlalchemy import Table,Column,Integer,String
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import engine

from flask import Flask,g,request,Response,make_response,render_template,url_for,redirect,flash,session
from werkzeug.security import generate_password_hash,check_password_hash

# config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB`_PORT')
APP_SECRET = os.getenv('APP_SECRET')
JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = os.getenv('ALGORITHM')

genai.configure(api_key=GOOGLE_API_KEY)


db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = engine.URL.create('postgresql+psycopg2',DB_USER,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)
app.secret_key = APP_SECRET

db.init_app(app)
# CORS(app,supports_credentials = True);

model = genai.GenerativeModel('gemini-pro')

class Users(db.Model):
    email = Column(String,primary_key=True)
    uhash = Column(String)
    
    
with app.app_context():
    db.create_all()


@app.before_request
def verifyUser():
    if '/static/' in request.path:
        return

    user = {}
    token = request.cookies.get('token',None)
    if token:
        try:
            payload = jwt.decode(token,key=JWT_SECRET,algorithms=ALGORITHM)
            user["isAuthenticated"] = True
            user["profile"] = copy.deepcopy(payload)
            print("woo")

        except jwt.exceptions.InvalidTokenError:
            user["isAuthenticated"] = False
            user["profile"] = None
            print("booo")
            
    else:
        user["isAuthenticated"] = False
        user["profile"] = None
    
    g.user = user


def generate_token(email):
    exp_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=60)
    jwt_payload = { "email":email,"exp":exp_time }
    token = jwt.encode(payload=jwt_payload, key=JWT_SECRET, algorithm=ALGORITHM)
    return token


def login_required(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        user = g.get('user',None)

        if user and user["isAuthenticated"]:
            return f(*args,**kwargs)
        
        return redirect(url_for('login_page'))
    return wrapper


def login_not_required(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        user = g.get('user',None)
        # print(user)
        if user and user['isAuthenticated']:
            return redirect(url_for('home'))
        return f(*args,**kwargs)

    return wrapper


@app.get("/")
def home():
    print(g.get('user',None))
    return render_template('home.html')


# ---- authentication 

@app.get("/auth/login")
@login_not_required
def login_page():
    print(g.get('user',None))
    return render_template('login.html')


@app.post("/auth/login")
@login_not_required
def login():
    print(request.form)
    email:str = request.form.get('email', None)
    password:str = request.form.get('password', None)

    email = email.strip()
    password = password.strip()

    if (not email) or (not password):
        flash('Invalid Credentials!')
        # get_flashed_messages()
        return redirect(url_for('login_page'))


    res = db.session.execute(db.select(Users).where(Users.email == email)).scalars().all()

    if (not (len(res) > 0)) or (not check_password_hash(res[0].uhash, password)):
        flash('Invalid Credentials!')
        return redirect(url_for('login_page'))
    
    # generate JWT token and add it to cookies
    token = generate_token(email)
    
    resp = make_response(redirect("/"))
    resp.set_cookie(key='token', value=token, path="/", httponly=True, max_age=60, samesite="lax")

    return resp


@app.get("/auth/logout")
@login_required
def logout():
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('token','',expires=0)
    return resp


@app.get("/auth/signup")
@login_not_required
def signup_page():
    return render_template('signup.html')


@app.post("/auth/signup")
@login_not_required
def signup():
    print(request.form)
    email:str = request.form.get('email', None)
    password:str = request.form.get('password', None)
    
    email = email.strip()
    password = password.strip()

    if (not email) or (not password):
        flash('Invalid Credentials!')
        # get_flashed_messages()
        return redirect(url_for('login_page'))


    res = db.session.execute(db.select(Users).where(Users.email == email)).scalars().all()

    if len(res) > 0:
        # user with given email already exists
        flash('Email Is Not Avaliable!')
        return redirect(url_for('login_page'))

    phash = generate_password_hash(password, salt_length = 10)
    new_user = Users(email = email, uhash = phash)

    db.session.add(new_user)
    db.session.commit()

    # generate JWT token and add it to cookies
    token = generate_token(email)
    
    resp = make_response(redirect("/"))
    resp.set_cookie(key = 'token',value = token,path="/",max_age=60,httponly=True)

    return resp


# ---- application

if __name__ == "__main__":
    app.run(debug=True)