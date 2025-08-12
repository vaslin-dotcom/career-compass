import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env
load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

from resume_parser import *
from interviewer import *
from job_searcher import *
from job_roles_predictor import *




llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-8b-8192",
    temperature=0
)




if __name__ == "__main__":
    output=resume_parser(llm,"/workspaces/career-compass/RESUME_av.docx")
    skills_list=output['Parsed_Skills_List']
    evaluation = evaluate_multiple_skills(llm,skills_list)
    predicted_roles=job_predictor(llm,evaluation)
    print(predicted_roles)





