from resume_builder import app
from flask import g,render_template

@app.get("/")
def home():
    user = g.get('user',None)
    email = ""
    if user and user["isAuthenticated"]:
        email = user['profile']['email']
    
    return render_template('home.html',email=email)