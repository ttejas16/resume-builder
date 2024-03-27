from resume_builder import app
from flask import render_template

@app.get("/create")
def create_resume():
    return render_template("create.html")