# app/main.py
from fastapi import FastAPI
from app.routes import calls  # Import routes
from dotenv import load_dotenv

load_dotenv(override=True)  # Load environment variables from .env


app = FastAPI()
print("FastAPI application started")
# Register routes
app.include_router(calls.router)
print("Routes registered")
