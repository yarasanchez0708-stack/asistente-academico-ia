from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from uuid import uuid4

from models import Task, TaskCreate

app = FastAPI(
    title="Academic Assistant API",
    description="API to manage academic tasks with AI",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- In-memory storage (initial phase) ---
tasks_db: List[Task] = []


# --- Endpoints ---

@app.get("/")
def root():
    return {"message": "Academic Assistant API is running ✓", "version": "0.1.0"}


@app.get("/tasks", response_model=List[Task])
def list_tasks(subject: Optional[str] = None, completed: Optional[bool] = None):
    result = tasks_db
    if subject:
        result = [t for t in result if t.subject.lower() == subject.lower()]
    if completed is not None:
        result = [t for t in result if t.completed == completed]
    return result


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    new_task = Task(id=str(uuid4()), **task.model_dump())
    tasks_db.append(new_task)
    return new_task


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: str):
    for task in tasks_db:
        if task.id == task_id:
            task.completed = True
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    global tasks_db
    original_len = len(tasks_db)
    tasks_db = [t for t in tasks_db if t.id != task_id]
    if len(tasks_db) == original_len:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


@app.get("/tasks/stats/summary")
def summary():
    total = len(tasks_db)
    completed = sum(1 for t in tasks_db if t.completed)
    return {
        "total": total,
        "completed": completed,
        "pending": total - completed
    }
