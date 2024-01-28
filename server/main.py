import os
import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask,request
from flask_cors import CORS, cross_origin

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY');
genai.configure(api_key=GOOGLE_API_KEY)


app  = Flask(__name__)
CORS(app);

@app.route("/resume/learn/<prompt>", methods = ["GET"])
def get_resume_data(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt);
    
    print(response.text)
    return 

if __name__ == "__main__":
    app.run(debug=True)