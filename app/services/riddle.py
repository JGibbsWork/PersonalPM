# app/services/openai_service.py
import openai
import requests
from app.config import RIDDLE_API_URL

def fetch_riddle():
    response = requests.get(RIDDLE_API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch riddle. Status code: {response.status_code}")
