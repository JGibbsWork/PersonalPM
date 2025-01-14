from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class Task(BaseModel):
    id: int
    title: str
    description: str
    due_date: datetime
    completed: bool = False

tasks = []

@router.post("/")
async def create_task(task: Task):
    tasks.append(task)
    return {"message": "Task created successfully", "task": task}

@router.get("/")
async def get_tasks():
    return tasks
