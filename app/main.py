# app/main.py
from fastapi import FastAPI
from app.routes import calls  # Import routes
from app.services import openai_service

app = FastAPI()
print("FastAPI application started")
# Register routes
app.include_router(calls.router)
print("Routes registered")
