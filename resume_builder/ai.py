import google.generativeai as genai
from flask import jsonify,request
from resume_builder import app,GOOGLE_API_KEY
from resume_builder.authentication import login_required


genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@login_required
@app.post("/generate-text")
def generateText():
    
    search_text = request.get_json()["searchText"]
    response = model.generate_content(search_text)

    return jsonify(response.text)
