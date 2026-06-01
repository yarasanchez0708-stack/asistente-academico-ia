# Reporte de Control Arquitectónico Intermedio

**Fecha:** Mayo 2026
**Sprint:** Issues #2 — #5
**Herramienta:** Análisis manual + ChatGPT (flujo adaptado, equivalente a `/improve-codebase-architecture`)

> Este documento registra la pausa obligatoria de auditoría arquitectónica ejecutada tras completar los primeros issues del sprint, siguiendo el **Paso 3** del flujo de la Tarea 2. El objetivo es identificar módulos superficiales, lógica dispersa y dependencias cíclicas antes de acumular deuda técnica irreversible en los issues de mayor complejidad (#6, #7, #8).

---

## 1. Diagnóstico Inicial

### Estructura analizada

```
asistente-academico-ia/
├── backend/
│   ├── __init__.py
│   ├── main.py          ⚠️  Rutas + lógica de negocio + estado mezclados
│   └── models.py        ✅  Modelos Pydantic separados
├── frontend/
│   └── index.html       ⚠️  HTML + CSS + JS en un solo archivo
├── .env.example
├── .gitignore
├── README.md
├── client-brief.md
└── requirements.txt
```

### Problemas identificados

Siguiendo la terminología de Ousterhout en *A Philosophy of Software Design*:

| # | Problema | Clasificación Ousterhout | Riesgo |
|---|---|---|---|
| 1 | `main.py` mezcla rutas, lógica de negocio y almacenamiento en memoria | **Módulo Superficial** — su interfaz es tan compleja como su implementación | Alto: cualquier cambio en el almacenamiento rompe las rutas |
| 2 | `index.html` contiene HTML, CSS y JS en un solo archivo | **Módulo Superficial** — no oculta nada, expone toda su complejidad | Medio: imposible testear la lógica JS de forma aislada |
| 3 | Sin capa de servicios entre rutas y datos | **Information Leakage** — los detalles del almacenamiento se filtran hacia las rutas | Alto: bloquea la implementación de JWT (#7) e historial persistente (#8) |

---

## 2. Propuestas de los 3 Sub-agentes

El agente simuló tres perspectivas arquitectónicas en paralelo, cada una con un enfoque radicalmente distinto para resolver los problemas identificados.

---

### Sub-agente A — Separación completa por capas (MVC estricto)

**Propuesta:** Reorganizar el backend en tres capas formales:

```
backend/
├── routers/
│   └── tasks.py          # Solo rutas FastAPI (sin lógica)
├── services/
│   └── task_service.py   # Lógica de negocio pura
├── repositories/
│   └── task_repo.py      # Acceso a datos (memoria → BD futura)
├── models.py
└── main.py               # Solo configuración de la app
```

**Argumento:** Este diseño produce **módulos profundos** en el sentido de Ousterhout: cada capa oculta su complejidad detrás de una interfaz simple. El `task_service.py` no sabe si los datos vienen de memoria o de una base de datos — eso es responsabilidad exclusiva del repositorio.

**Ventaja:** Máxima separación de responsabilidades. Los issues #7 (JWT) y #8 (historial) se implementarían sin tocar las rutas existentes.

**Desventaja:** Introduce tres niveles de indirección para un MVP con cinco endpoints. Ousterhout advierte contra la **complejidad cognitiva innecesaria**: si la abstracción no oculta complejidad real, solo añade ruido.

---

### Sub-agente B — Separación mínima funcional (router extraction)

**Propuesta:** Extraer únicamente las rutas a un módulo separado:

```
backend/
├── routers/
│   └── tasks.py   # Endpoints de tareas extraídos de main.py
├── models.py
└── main.py        # Solo configuración: app = FastAPI(), include_router()
```

**Argumento:** Esta es la intervención de menor riesgo con mayor impacto inmediato. Resuelve el problema crítico de `main.py` como módulo superficial sin introducir abstracciones prematuras. Siguiendo a Ousterhout: *"El mejor diseño es el más simple que funciona"*.

**Ventaja:** Mejora significativa en legibilidad y mantenibilidad con cambio mínimo. `main.py` queda como un módulo profundo: oculta la complejidad de configuración detrás de tres líneas.

**Desventaja:** La lógica de negocio sigue acoplada a las rutas dentro de `routers/tasks.py`. No resuelve el problema de Information Leakage hacia los issues futuros.

---

### Sub-agente C — Refactorizar el frontend primero

**Propuesta:** Mantener el backend temporalmente y atacar el módulo superficial más visible:

```
frontend/
├── index.html     # Solo estructura HTML semántica
├── styles.css     # Presentación separada
└── app.js         # Toda la lógica de comportamiento
```

**Argumento:** El frontend monolítico es el módulo superficial más evidente del sistema. La separación HTML/CSS/JS es la aplicación directa del principio de **ocultamiento de información**: `index.html` no debe saber nada sobre cómo se renderizan los estilos ni cómo se procesan los eventos.

**Ventaja:** Mejora la mantenibilidad del frontend inmediatamente. Permite testear `app.js` de forma aislada en el futuro.

**Desventaja:** No resuelve el riesgo arquitectónico principal (el acoplamiento en `main.py`) que bloquea los issues #7 y #8.

---

## 3. Decisión Final — Solución Híbrida

**Se adopta Sub-agente B + Sub-agente C en secuencia**, priorizando el frontend (C) primero por ser el cambio más seguro, luego la extracción del router (B).

### Justificación técnica

Aplicando el marco de Ousterhout, la decisión se fundamenta en dos principios:

1. **Módulos Profundos sobre Módulos Superficiales:** La propuesta del Sub-agente A crea la arquitectura más correcta a largo plazo, pero introduce tres niveles de indirección donde actualmente no hay complejidad suficiente que justificarlos. Ousterhout es explícito: una abstracción que no oculta complejidad real es un **módulo superficial disfrazado de arquitectura**.

2. **Gestión táctica de la complejidad:** El Sub-agente B resuelve el problema de mayor riesgo (el acoplamiento de `main.py`) con el menor costo de implementación. La separación en `routers/tasks.py` produce un `main.py` genuinamente profundo: tres líneas de interfaz que ocultan toda la configuración de la aplicación.

### Secuencia de implementación

| Orden | Acción | Issue relacionado | Resultado esperado |
|---|---|---|---|
| 1° | Separar `app.js` y `styles.css` de `index.html` | Refactor previo a #5 | Frontend testeable, HTML limpio |
| 2° | Extraer rutas a `backend/routers/tasks.py` | Previo a #7 | `main.py` como módulo de configuración puro |
| 3° | Evaluar capa de servicios | Al iniciar #7 o #8 | Decidir si la complejidad justifica el repositorio |

---

## 4. Resultado de la Implementación

### Cambios aplicados

Los siguientes commits registran la aplicación de la decisión híbrida:

- `refactor: separate models layer, translate to English, connect frontend to API` (21 mayo)
- `refactor: move JS logic to app.js, link from index.html` (21 mayo)

### Estado post-refactor

```
frontend/
├── index.html     ✅  Solo estructura HTML
└── app.js         ✅  Lógica JS separada

backend/
├── main.py        ✅  Configuración de la app
├── models.py      ✅  Modelos Pydantic
└── routers/       🔄  Pendiente para sprint siguiente
```

### Estado de los tests

- Backend corre correctamente con `uvicorn main:app --reload`
- Todos los endpoints responden según documentación en `/docs`
- Frontend se conecta correctamente al backend vía `fetch()`
- Sin regresiones introducidas por el refactor

---

## 5. Issues desbloqueados tras el checkpoint

| Issue | Estado previo | Estado post-checkpoint | Razón del desbloqueo |
|---|---|---|---|
| #5 — Backend y Frontend base | Bloqueado | **Desbloqueado** ✅ | Frontend separado permite integración limpia |
| #6 — Exportar tareas a PDF | Bloqueado | **Desbloqueado** ✅ | `app.js` separado facilita llamada al endpoint de export |
| #7 — Autenticación JWT | Bloqueado | **Parcialmente desbloqueado** 🔄 | Requiere extracción de routers antes de implementar middleware |
| #8 — Chat con historial persistente | Bloqueado | **Bloqueado** ⏳ | Depende de #7 (autenticación) para asociar historial al usuario |
