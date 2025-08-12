
import os
from dotenv import load_dotenv
import requests
import os
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage


# Load environment variables from .env
load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
def search_jobs(
    query="",                     # job role or keywords
    location="",                  # city/region
    country="in",                 # country code
    page=1,
    num_pages=1,
    date_posted="all",            # "all", "today", "3days", "week", "month"
    employment_types=None,        # ["fulltime","parttime","contract","internship"]
    remote_jobs_only=False,
    sort_by="date_posted",        # "date_posted", "relevance"
    order="desc",                  # "asc", "desc"
    radius=None,                  # search distance
    experience_level=None,        # "junior", "mid", "senior"
    skills=None,                  # list of skills to match
    industry=None,                # sector/industry keyword
    salary_min=None,              # minimum salary
    salary_max=None,              # maximum salary
    language=None,                 # required language
    company_type=None              # "startup", "MNC", etc.
):
    """
    Search jobs using JSearch API with extra local filtering.
    """

    # API request setup
    url = "https://jsearch.p.rapidapi.com/search"
    params = {
        "query": query,
        "page": page,
        "num_pages": num_pages,
        "country": country,
        "location": location,
        "sort_by": sort_by,
        "order": order
    }
    if date_posted:
        params["date_posted"] = date_posted
    if employment_types:
        params["employment_types"] = ",".join(employment_types)
    if remote_jobs_only:
        params["remote_jobs_only"] = "true"
    if radius:
        params["radius"] = radius

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return f"Error: {response.status_code} - {response.text}"

    data = response.json()
    jobs = data.get("data", [])
    if not jobs:
        return "No jobs found."

    # Local filtering
    filtered_jobs = []
    for job in jobs:
        title = job.get("job_title", "").lower()
        description = (job.get("job_description") or "").lower()
        salary_min_api = job.get("job_min_salary")
        salary_max_api = job.get("job_max_salary")

        # Experience filter
        if experience_level:
            if not any(keyword.lower() in title or keyword.lower() in description for keyword in experience_level):
                continue

        # Skills filter
        if skills and not any(skill.lower() in description for skill in skills):
            continue

        # Industry filter
        if industry and industry.lower() not in description:
            continue

        # Salary filter
        if salary_min and salary_min_api and salary_min_api < salary_min:
            continue
        if salary_max and salary_max_api and salary_max_api > salary_max:
            continue

        # Language filter
        if language and language.lower() not in description:
            continue

        # Company type filter
        if company_type and company_type.lower() not in (job.get("employer_name") or "").lower():
            continue

        filtered_jobs.append(job)

    # Format results
    results = []
    for i, job in enumerate(filtered_jobs, start=1):
        title = job.get("job_title", "N/A")
        company = job.get("employer_name", "Unknown")
        link = job.get("job_apply_link", "#")
        city = (
            job.get("job_location")
            or ", ".join(filter(None, [
                job.get("job_city"),
                job.get("job_state"),
                job.get("job_country")
            ]))
            or ("Remote" if job.get("job_is_remote") else "Unknown")
        )
        results.append(
            f"{i}. **{title}**\nCompany: {company}\nLocation: {city}\n\n[Apply here]({link})"
        )

    return "\n\n".join(results)






def filter(
    llm,query, location, country, page, num_pages, date_posted,
    employment_types, remote_jobs_only, sort_by, order, radius,
    experience_level, skills, industry, salary_min, salary_max,
    language, company_type
):


    job_list_markdown = search_jobs(
        query=query,
        location=location,
        country=country,
        page=page,
        num_pages=num_pages,
        date_posted=date_posted,
        employment_types=employment_types,
        remote_jobs_only=remote_jobs_only,
        sort_by=sort_by,
        order=order,
        radius=radius,
        experience_level=experience_level,
        skills=skills,
        industry=industry,
        salary_min=salary_min,
        salary_max=salary_max,
        language=language,
        company_type=company_type
    )

    if job_list_markdown.startswith("Error") or job_list_markdown == "No jobs found.":
        print(job_list_markdown)
        return

    prompt = (
    f"Here are some current job openings for '{query}' in {location}:\n\n"
    f"{job_list_markdown}\n\n"
    "Please provide a brief summary of these jobs with region of job, but keep the original job application links in your output. "
    "After each job summary, include the 'Apply here' link from the original list."
    "Output format\n"
    "<city>:<job role>,<company>:\n\n<summary>\n\n "
    "\n\n[APPLY LINK]<link>\n"

)


    # Wrap prompt as HumanMessage inside a list, then call invoke()
    response = llm.invoke([HumanMessage(content=prompt)])

    # Access the content directly from the AIMessage object
    print(response.content)

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