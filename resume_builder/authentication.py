import datetime
import jwt
import copy 

from resume_builder.models.User import User
from resume_builder import app,db,JWT_SECRET,ALGORITHM
from functools import wraps

from flask import Flask,g,request,Response,make_response,render_template,url_for,redirect,flash,session
from werkzeug.security import generate_password_hash,check_password_hash



# middlewares
def generate_token(email):
    exp_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60)
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


@app.before_request
def verify_user():
    if '/static/' in request.path:
        return

    user = {}
    token = request.cookies.get('token',None)
    if token:
        try:
            payload = jwt.decode(token,key=JWT_SECRET,algorithms=ALGORITHM)
            user["isAuthenticated"] = True
            user["profile"] = copy.deepcopy(payload)
            # print("woo")

        except jwt.exceptions.InvalidTokenError:
            user["isAuthenticated"] = False
            user["profile"] = None
            # print("booo")
            
    else:
        user["isAuthenticated"] = False
        user["profile"] = None
    
    g.user = user

@app.context_processor
def add_user():
    user = g.get("user",{ "isAuthenticated":False, "profile":None });
    return dict(user=user)


# login route   
@app.get("/auth/login")
@login_not_required
def login_page():
    # print(g.get('user',None))
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
        flash('Invalid Credentials!',category='error')
        # get_flashed_messages()
        return redirect(url_for('login_page'))


    res = db.session.execute(db.select(User).where(User.email == email)).scalars().all()

    if (not (len(res) > 0)) or (not check_password_hash(res[0].hash, password)):
        flash('Invalid Credentials!',category='error')
        return redirect(url_for('login_page'))
    
    # generate JWT token and add it to cookies
    token = generate_token(email)
    
    resp = make_response(redirect("/"))
    resp.set_cookie(key='token', value=token, path="/", httponly=True, max_age=60*60, samesite="lax")

    return resp


# signup routes
@app.post("/auth/signup")
@login_not_required
def signup():
    # print(request.form)
    email:str = request.form.get('email', None)
    password:str = request.form.get('password', None)
    first_name:str = request.form.get('firstName', None)
    last_name:str = request.form.get('lastName', None)
    
    email = email.strip()
    password = password.strip()
    first_name = first_name.strip()
    last_name = last_name.strip()

    if (not email) or (not password) or (not first_name) or (not last_name):
        flash('Please Fill All Details!',category='error')
        # get_flashed_messages()
        return redirect(url_for('login_page'))


    res = db.session.execute(db.select(User).where(User.email == email)).scalars().all()

    if len(res) > 0:
        # user with given email already exists
        flash('Email Is Not Avaliable!',category='error')
        return redirect(url_for('login_page'))

    phash = generate_password_hash(password, salt_length = 10)
    new_user = User(first_name=first_name,last_name=last_name,email=email,hash=phash)

    db.session.add(new_user)
    db.session.commit()


    flash('User Registered!',category='message')
    return redirect(url_for('login_page'))


@app.get("/auth/logout")
@login_required
def logout():
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('token' ,value='' , path="/", httponly=True, samesite='lax', max_age=0)
    return resp