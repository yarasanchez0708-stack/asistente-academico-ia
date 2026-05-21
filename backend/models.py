from pydantic import BaseModel
from typing import Optional
from datetime import date


class TaskCreate(BaseModel):
    title: str
    subject: str
    due_date: date
    priority: Optional[str] = "medium"  # high, medium, low
    description: Optional[str] = ""


class Task(TaskCreate):
    id: str
    completed: bool = False
