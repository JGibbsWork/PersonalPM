# app/main.py
from fastapi import FastAPI
from app.routes import calls  # Import routes

app = FastAPI()

# Register routes
app.include_router(calls.router)
