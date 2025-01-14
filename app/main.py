from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import tasks, notifications
from db import init_db

# Create FastAPI instance
app = FastAPI(
    title="Daily Goals Tracker",
    description="An app for managing daily tasks, AI summaries, and Twilio notifications.",
    version="1.0.0",
)

# CORS Middleware (if you plan to connect with a frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])

# Run database initialization
@app.on_event("startup")
async def startup_event():
    print("Initializing database...")
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down application...")

# Root endpoint for health check
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Daily Goals Tracker API!"}
