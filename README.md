# 🎓 Asistente Académico Inteligente

Aplicación web con IA para ayudar a estudiantes a organizar tareas, consultar dudas académicas y mejorar su productividad durante el semestre.

---

## 📋 Descripción del Proyecto

El **Asistente Académico Inteligente** es una aplicación full-stack que combina un backend en Python/FastAPI con un frontend en HTML/JavaScript. Permite a estudiantes:

- Registrar y gestionar tareas académicas por materia y fecha de entrega
- Consultar un asistente IA para resolver dudas de estudio
- Recibir recordatorios y priorización automática de tareas pendientes

El proyecto se desarrolla de forma incremental durante el semestre, usando **Claude Code** como herramienta principal de desarrollo.

---

## 🛠️ Tecnologías

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3.11+, FastAPI, Uvicorn |
| Frontend | HTML5, CSS3, JavaScript (Vanilla) |
| IA | Anthropic API (Claude) |
| Control de versiones | Git + GitHub |
| Dev tool | Claude Code |

---

## 📁 Estructura del Proyecto
asistente-academico-ia/
├── backend/
│   └── main.py          # Punto de entrada FastAPI
├── frontend/
│   └── index.html       # Interfaz de usuario
├── README.md
├── client-brief.md
└── requirements.txt

---

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/yarasanchez0708-stack/asistente-academico-ia.git
cd asistente-academico-ia
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

### 3. Ejecutar el backend

```bash
cd backend
uvicorn main:app --reload
```

El servidor corre en `http://localhost:8000`. Documentación automática en `http://localhost:8000/docs`.

### 4. Abrir el frontend

Abrir `frontend/index.html` directamente en el navegador.

---

## 🤖 Cómo se aplicó el flujo de Claude Code (AFK Agent)

Este proyecto sigue el flujo descrito en [Running Your AFK Agent](https://www.aihero.dev/running-your-afk-agent-a9l1u):

### 1. Client Brief primero
Antes de escribir código, se redactó un `client-brief.md` claro con el problema, objetivo, alcance y criterios de éxito. Esto sirve como contexto de referencia para Claude Code en cada sesión.

### 2. Issues como unidad de trabajo
Cada feature se traduce en un GitHub Issue bien redactado. Claude Code recibe el issue como tarea concreta en lugar de instrucciones vagas.

### 3. Sesiones AFK (autónomas)
Se lanza Claude Code con la instrucción de trabajar sobre un issue específico, se deja correr de forma autónoma, y se revisa el resultado al final.

### 4. Revisión y commit
Después de cada sesión AFK se revisa el diff, se ajusta lo necesario, y se hace commit con referencia al issue (`closes #2`).

### 5. Iteración incremental
El proyecto no se intenta terminar de una sola vez. Cada entrega del semestre agrega una capa funcional sobre la anterior.

---

## 📅 Estado actual

- [x] Estructura inicial del proyecto
- [x] Backend básico con FastAPI (CRUD de tareas)
- [x] Frontend inicial con listado y creación de tareas
- [ ] Integración con Anthropic API para respuestas IA
- [ ] Sistema de priorización automática
- [ ] Autenticación de usuarios

---

## 👩‍💻 Autora

**Yara Sánchez** — Proyecto Integrador, semestre 2026-1

---

## API Endpoints

La API backend está desarrollada con FastAPI y expone endpoints REST para la gestión de tareas académicas.

### Base URL

http://127.0.0.1:8000

### Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /tasks | Obtener todas las tareas |
| POST | /tasks | Crear una nueva tarea |
| PATCH | /tasks/{task_id}/completar | Marcar tarea como completada |
| DELETE | /tasks/{task_id} | Eliminar una tarea |
| GET | /tasks/stats/resumen | Estadísticas de tareas |

### Documentación Automática
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## Buenas Prácticas y Convenciones

### Backend
- Separación de modelos Pydantic en `models.py`
- Uso de tipado estático con Python 3.11+
- Variables sensibles manejadas mediante `.env`

### Frontend
- Estructura simple basada en HTML/CSS/JS vanilla
- Comunicación mediante API REST

### Convención de Commits
| Prefijo | Uso |
|---------|-----|
| `feat(#N)` | Nueva funcionalidad vinculada a issue |
| `fix(#N)` | Corrección de bug |
| `docs` | Documentación |
| `refactor` | Refactorización de código |
