# Career Compass – AI-Powered Job Role Predictor & Job Searcher

## 📌 Overview
Career Compass is an AI-driven backend system that analyzes a candidate’s resume or profile data,conducts a friendly interview, predicts suitable job roles with confidence scores, and searches for relevant job postings online.  
This repository currently showcases the **backend logic only** for demonstration purposes.

I am actively working on integrating a frontend UI(with voice based interaction) and deploying the application on a server with an **LLM running locally**, to eliminate dependency on API keys and make it a fully functional scalable app.

---

## ⚙️ Backend Logic

### 1. **LLM Integration**
- **Model:** LLaMA 3 8B (hosted on Groq API)  
- **Usage:**  
  - Given extracted resume text, the LLM predicts suitable job roles based on skills, experience, and domain knowledge.  
  - Output includes multiple job roles ranked by relevance with associated confidence scores.  
- **Tech Used:**  
  - **LangChain** – for prompt construction and model interaction  
  - **Groq API** – for high-speed inference on LLaMA 3

---

### 2. **Job Search**
- **API Provider:** JSearch via **RapidAPI**  
- **Usage:**  
  - Takes a selected job role and queries for matching job postings (location & filters can be customized).  
  - Returns job title, company, location, and application link.

---

## 🖥️ Exhibition Logic (Demo Mode)

Since API keys cannot be exposed publicly and live deployment would require a secure backend, this repository uses a **two-step manual process** for demonstration:

1. **Run `app.py`**
   - Loads sample resume data (or user-provided input)
   - Conducts interview on the skills collected from resume(which are not explitely mentioned also,such as from projects,achievements etc) using Groq LLaMA
   - Sends it to the Groq LLaMA 3 model via LangChain
   - Prints predicted job roles with confidence scores

2. **Run `job_searcher.py`**
   - User manually enters one of the predicted roles from `app.py` output
   - Fetches job postings from JSearch (RapidAPI) and displays them in console

This separation allows you to see the **core logic** without exposing sensitive credentials.

---

## 📚 Tech Stack & Frameworks

- **Python** – Core development language  
- **LangChain** – Orchestration framework for LLM prompts & pipelines  
- **Groq API** – For running LLaMA 3 model (fast inference)  
- **RapidAPI (JSearch)** – Job search API for live job listings  
- **Requests** – API calls  
- **JSON** – Structured data handling  
- **dotenv** – Secure environment variable management

---

## 🚀 Roadmap / Work in Progress

I am actively working on:
- **Frontend Integration** – Building an interactive UI with Streamlit/Vue.js
- **Secure Deployment** – Running LLM on my own server instead of using Groq API for scalability
- **Automated Pipeline** – Passing predicted roles directly into the job search module without manual entry
- **User Authentication & Rate Limiting** – For safe public access
- **Cloud Hosting** – Deploying the complete app for public demo

---

## 📷 Sample Output

**Step 1 – Predicted Roles:**(after conducting interview)
Data Scientist – 0.92

Machine Learning Engineer – 0.88

AI Researcher – 0.85


**Step 2 – Job Search Results:**(fill the details based on above outcomes and other requirements in job_searcher.py)
Title: Machine Learning Engineer
Company: ABC Tech
Location: Bangalore, India
Link: https://example.com/job123



---

## 📄 Disclaimer
This repository is for educational and demonstration purposes only.  
API keys for Groq and RapidAPI are **not included** for security reasons.
