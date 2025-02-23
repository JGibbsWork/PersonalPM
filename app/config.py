# app/config.py
from dotenv import load_dotenv
import os

load_dotenv(override=True)  # Load environment variables from .env

# Twilio
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
TO_PHONE_NUMBER = os.getenv("TO_PHONE_NUMBER")

# OpenAI
OPENAI_API_KEY = os.getenv("OPEN_AI_KEY")

# Additional things

EVENTS_API_URL = os.getenv("EVENTS_API_URL")
RIDDLE_API_URL = os.getenv("RIDDLE_API_URL")
MONGO_URI = os.getenv("MONGO_URI")
NGROK_URL = os.getenv("NGROK_URL")