# Reporte de Control Arquitectónico

**Fecha:** Mayo 2026  
**Sprint:** Issues #2 — #4  
**Herramienta:** Análisis manual + ChatGPT (flujo adaptado)

---

## Diagnóstico Inicial

Tras completar los issues #2, #3 y #4, se realizó una pausa para auditar la arquitectura del proyecto antes de continuar con issues más complejos.

### Estructura actual analizada

asistente-academico-ia/
├── backend/
│   ├── init.py
│   ├── main.py        # Rutas + lógica de negocio mezcladas
│   └── models.py      # Modelos Pydantic separados ✅
├── frontend/
│   └── index.html     # HTML + CSS + JS en un solo archivo
├── .env.example
├── .gitignore
├── README.md
├── client-brief.md
└── requirements.txt

### Problemas identificados

1. **main.py tiene demasiadas responsabilidades** — mezcla rutas, lógica de negocio y almacenamiento en memoria
2. **Frontend monolítico** — todo el HTML, CSS y JS está en un solo archivo index.html
3. **Sin capa de servicios** — no hay separación entre rutas y lógica de negocio

---

## Propuestas de los 3 Sub-agentes

### Sub-agente A — Separación por capas (MVC)
Propone reorganizar el backend en tres capas:
- `routers/tasks.py` — solo rutas FastAPI
- `services/task_service.py` — lógica de negocio
- `repositories/task_repo.py` — acceso a datos

**Ventaja:** máxima separación de responsabilidades  
**Desventaja:** mayor complejidad para un MVP

### Sub-agente B — Separación mínima funcional
Propone solo extraer las rutas a un router separado:
- `backend/routers/tasks.py` — endpoints de tareas
- `backend/main.py` — solo configuración de la app

**Ventaja:** mejora significativa con cambio mínimo  
**Desventaja:** la lógica de negocio sigue mezclada con las rutas

### Sub-agente C — Refactorizar frontend
Propone mantener el backend como está y enfocarse en separar el frontend:
- `frontend/index.html` — solo estructura HTML
- `frontend/styles.css` — estilos separados
- `frontend/app.js` — lógica JavaScript separada

**Ventaja:** mejora la mantenibilidad del frontend  
**Desventaja:** no resuelve los problemas del backend

---

## Decisión Final

Se adopta la propuesta del **Sub-agente B** como siguiente paso — es la mejora más impactante con el menor riesgo de romper funcionalidad existente.

**Acción:** Crear `backend/routers/tasks.py` con todas las rutas y simplificar `main.py` a solo configuración de la app FastAPI.

**Justificación:** El proyecto está en fase MVP. Una separación completa en 3 capas (Sub-agente A) es prematura. Separar solo los routers da una base limpia para escalar en los siguientes issues sin acumular deuda técnica.

---

## Estado de los Tests

- Backend corre correctamente con `uvicorn main:app --reload`
- Todos los endpoints responden según documentación en `/docs`
- Frontend se conecta correctamente al backend via fetch()
