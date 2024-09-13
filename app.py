from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from dotenv import load_dotenv
import os
app = Flask(__name__)
CORS(app)


openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    # receive the data from the client
    data = request.json
    # extract the job details 
    job_details = data["jobDetails"]
    # get the user skills 
    # this should come from the db, I will prompt the user to input their skills before using
    # the tool
    user_skills = data["userSkills"]

    #  prompt ai to write a content for the user 
    prompt = f"""
    Create a professional resume for the following job:
    
    Job Title: {job_title}
    Job Description: {job_description}
    
    The candidate has the following skills: {user_skills}
    
    Format the resume with appropriate sections such as Summary, Skills, Experience, and Education.
    """
    try:
        response = openai.Completion.Create( 
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=500,
        n=1,
        top=None,
        temperature=0.7
        )
        generated_resume = response.choice[0].text.strip()
        return jsonify({"resume": generated_resume})

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"})

    
    
if __name__ == "__main__":
    app.run(debug=True)

