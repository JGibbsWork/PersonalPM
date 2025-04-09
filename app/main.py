# app/main.py
from fastapi import FastAPI
from app.routers import calls  
from dotenv import load_dotenv

load_dotenv(override=True)  
print("variables loaded")

app = FastAPI()
print("FastAPI application started")
app.include_router(calls.router)
print("Routes registered")

@app.get("/")
async def root():
    return {"message": "PersonalPM is alive"}
