from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from uuid import uuid4

app = FastAPI(
    title="Asistente Académico API",
    description="API para gestionar tareas académicas con IA",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelos ---

class TaskCreate(BaseModel):
    titulo: str
    materia: str
    fecha_entrega: date
    prioridad: Optional[str] = "media"  # alta, media, baja
    descripcion: Optional[str] = ""

class Task(TaskCreate):
    id: str
    completada: bool = False

# --- Almacenamiento en memoria (fase inicial) ---

tasks_db: List[Task] = []

# --- Endpoints ---

@app.get("/")
def root():
    return {"mensaje": "API del Asistente Académico funcionando ✓", "version": "0.1.0"}

@app.get("/tasks", response_model=List[Task])
def listar_tareas(materia: Optional[str] = None, completada: Optional[bool] = None):
    resultado = tasks_db
    if materia:
        resultado = [t for t in resultado if t.materia.lower() == materia.lower()]
    if completada is not None:
        resultado = [t for t in resultado if t.completada == completada]
    return resultado

@app.post("/tasks", response_model=Task, status_code=201)
def crear_tarea(tarea: TaskCreate):
    nueva_tarea = Task(id=str(uuid4()), **tarea.model_dump())
    tasks_db.append(nueva_tarea)
    return nueva_tarea

@app.get("/tasks/{task_id}", response_model=Task)
def obtener_tarea(task_id: str):
    tarea = next((t for t in tasks_db if t.id == task_id), None)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea

@app.patch("/tasks/{task_id}/completar", response_model=Task)
def completar_tarea(task_id: str):
    for tarea in tasks_db:
        if tarea.id == task_id:
            tarea.completada = True
            return tarea
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@app.delete("/tasks/{task_id}")
def eliminar_tarea(task_id: str):
    global tasks_db
    original_len = len(tasks_db)
    tasks_db = [t for t in tasks_db if t.id != task_id]
    if len(tasks_db) == original_len:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"mensaje": "Tarea eliminada correctamente"}

@app.get("/tasks/stats/resumen")
def resumen():
    total = len(tasks_db)
    completadas = sum(1 for t in tasks_db if t.completada)
    return {
        "total": total,
        "completadas": completadas,
        "pendientes": total - completadas
    }
