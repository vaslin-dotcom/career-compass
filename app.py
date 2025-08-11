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


def job_filters():
    exp = {
    "fresher": [
        "fresher", "graduate program", "trainee", "associate",
        "internship", "entry level", "campus hire",
        "0-1 years", "0-2 years", "no experience required"
    ],
    "junior": [
        "junior", "junior developer", "assistant", "support engineer",
        "1-2 years experience", "1-3 years experience", "early career"
    ],
    "mid": [
        "mid-level", "mid level", "experienced", "professional",
        "3-5 years experience", "3+ years", "4+ years",
        "staff engineer", "specialist"
    ],
    "senior": [
        "senior", "sr.", "lead", "principal", "architect",
        "5+ years experience", "7+ years", "senior engineer",
        "senior developer", "senior analyst"
    ],
    "executive": [
        "executive", "director", "vp", "vice president",
        "chief", "cto", "ceo", "head of", "cxo"
    ]
}

    
    # Store inputs in variables
    query = "Research Assistant"
    location = ""
    country = "in"
    page = 1
    num_pages = 10
    date_posted = "month"
    employment_types = ["fulltime"]
    remote_jobs_only = False
    sort_by = "date_posted"
    order = "desc"
    radius = None
    experience_level = exp["fresher"]+exp["junior"]
    skills = ''
    industry = ''
    salary_min = 50000
    salary_max =''
    language = ''
    company_type = ''
    filter(
    llm,query, location, country, page, num_pages, date_posted,
    employment_types, remote_jobs_only, sort_by, order, radius,
    experience_level, skills, industry, salary_min, salary_max,
    language, company_type
)

if __name__ == "__main__":
    output=resume_parser(llm,"/workspaces/career-compass/RESUME_av.docx")
    skills_list=output['Parsed_Skills_List']
    evaluation = evaluate_multiple_skills(llm,skills_list)
    