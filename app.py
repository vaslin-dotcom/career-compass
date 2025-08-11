import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env
load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
