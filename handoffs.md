# Bitácora de Transferencia de Contexto (Handoffs)

Este archivo registra los resúmenes de sesión generados al finalizar cada bloque de issues, siguiendo la técnica de **Handoff** para mitigar el desgaste de tokens en ventanas de contexto largas.

> **¿Por qué existe este archivo?**
> A medida que una sesión de desarrollo con IA se extiende, la acumulación de mensajes históricos introduce "ruido de tokens": el agente comienza a ignorar reglas de arquitectura establecidas al inicio, repite decisiones ya tomadas o introduce inconsistencias. El Handoff interrumpe ese ciclo: se genera un resumen ultra-compacto del estado real del sistema, se purga el historial, y la siguiente sesión arranca con contexto limpio y preciso.

---

## Handoff #1 — Issues #2, #3, #4

**Fecha:** 26 de mayo de 2026
**Issues completados:** #2 · #3 · #4
**Commits asociados:**
- `feat(#2): agregar __init__.py al módulo backend`
- `feat(#2): agregar .env.example`
- `feat(#2): agregar .gitignore`
- `feat(#3): mejorar client-brief con alcance, requisitos y roadmap`
- `feat(#4): agregar secciones API endpoints y buenas prácticas al README`

**Herramienta usada:** ChatGPT (flujo adaptado por recomendación del profesor)

---

### Componentes construidos

| Archivo | Descripción |
|---|---|
| `backend/__init__.py` | Módulo Python inicializado como paquete |
| `backend/models.py` | Modelos Pydantic extraídos de `main.py` |
| `.env.example` | Plantilla de variables de entorno (API keys, puerto) |
| `.gitignore` | Exclusión de `__pycache__`, `.env`, `venv/` |
| `client-brief.md` | Ampliado con alcance, requisitos no funcionales y roadmap técnico |
| `README.md` | Ampliado con tabla de endpoints y guía de buenas prácticas |

---

### Decisiones de arquitectura consolidadas

1. **Separación de modelos:** Los modelos Pydantic viven en `backend/models.py`, separados de la lógica de rutas en `main.py`. Esta decisión aplica el principio de **ocultamiento de información** de Ousterhout: el esquema de datos no debe estar acoplado a la capa de enrutamiento.
2. **Variables de entorno:** Las credenciales sensibles (API keys, configuración de base de datos) se manejan exclusivamente vía `.env`, nunca hardcodeadas.
3. **Comunicación frontend-backend:** El frontend se conecta al backend mediante `fetch()` hacia `http://localhost:8000`. Contrato de API definido antes de implementar la UI.
4. **Almacenamiento en memoria:** Para la fase MVP, el estado de las tareas se mantiene en un diccionario en memoria. Decisión deliberada y documentada — no deuda técnica accidental.

---

### Señales de ruido detectadas antes del handoff

Antes de cerrar esta sesión, el agente comenzó a sugerir agregar lógica de autenticación directamente dentro de `main.py`, mezclando responsabilidades que debían pertenecer a un módulo separado. Esta fue la señal de que el contexto se había degradado y era momento de ejecutar el handoff.

---

### Resumen de transferencia (texto para inicializar próxima sesión)

```
ESTADO DEL PROYECTO — Asistente Académico IA (Handoff #1)

Stack: Python + FastAPI (backend) · HTML/CSS/JS vanilla (frontend)
Comunicación: fetch() → http://localhost:8000

Archivos clave:
- backend/main.py → rutas FastAPI + lógica de negocio (pendiente refactor)
- backend/models.py → modelos Pydantic (separados ✓)
- frontend/index.html → HTML + CSS + JS (monolítico, pendiente separación)
- .env.example → plantilla de variables (API keys)

Decisiones inamovibles:
- Modelos Pydantic SIEMPRE en models.py, nunca en main.py
- Credenciales SIEMPRE en .env
- MVP sin base de datos (almacenamiento en memoria aceptado)

Issues pendientes: #5 (backend+frontend integrado), #6 (export PDF),
                   #7 (JWT auth), #8 (historial persistente)
Próximo issue a atacar: #5
```

---

## Handoff #2 — Refactor arquitectónico post-checkpoint

**Fecha:** 21 de mayo de 2026
**Commits asociados:**
- `refactor: separate models layer, translate to English, connect frontend to API`
- `refactor: move JS logic to app.js, link from index.html`

**Contexto:** Este handoff no surge de completar un issue específico, sino del **Punto de Control Arquitectónico** ejecutado tras el diagnóstico de `/improve-codebase-architecture`. Se detectaron dos módulos superficiales críticos que debían refactorizarse antes de continuar con los issues de mayor complejidad (#6, #7, #8).

---

### Cambios aplicados

| Cambio | Archivo origen | Archivo destino | Razón |
|---|---|---|---|
| Lógica JS extraída | `frontend/index.html` | `frontend/app.js` | Eliminar módulo superficial monolítico |
| Modelos traducidos al inglés | `backend/models.py` | `backend/models.py` | Consistencia con convenciones FastAPI/Pydantic |
| Frontend conectado a API real | `frontend/app.js` | — | Reemplazar datos mock por llamadas reales |

---

### Decisiones de arquitectura consolidadas

1. **Separación frontend:** El HTML es solo estructura. Toda lógica de comportamiento vive en `app.js`. Esta separación fue la recomendación del Sub-agente C del checkpoint arquitectónico, implementada como primer paso del refactor.
2. **Idioma del código:** El código fuente (variables, funciones, comentarios técnicos) se estandariza en inglés para mantener consistencia con las librerías del stack (FastAPI, Pydantic).
3. **Conexión real frontend-backend:** Se eliminaron los datos mockeados del frontend. Toda interacción pasa por los endpoints documentados en `/docs`.

---

### Señales de ruido detectadas antes del handoff

El agente comenzó a proponer agregar estilos CSS directamente en `app.js` mediante manipulación de `style` inline, rompiendo la separación recién establecida. Señal clara de degradación de contexto.

---

### Resumen de transferencia (texto para inicializar próxima sesión)

```
ESTADO DEL PROYECTO — Asistente Académico IA (Handoff #2)

Stack: Python + FastAPI (backend) · HTML + CSS + JS separados (frontend)
Comunicación: fetch() → http://localhost:8000 (conexión real, sin mocks)

Archivos clave:
- backend/main.py → rutas FastAPI (refactor pendiente: extraer a routers/)
- backend/models.py → modelos Pydantic en inglés ✓
- frontend/index.html → solo estructura HTML ✓
- frontend/app.js → toda la lógica JS ✓
- frontend/styles.css → (pendiente: extraer CSS de index.html)

Decisiones inamovibles:
- HTML = estructura, app.js = comportamiento, styles.css = presentación
- Código fuente en inglés (variables, funciones, comentarios técnicos)
- Sin datos mock: todo fetch() apunta a localhost:8000

Issues pendientes: #5 (backend+frontend integrado), #6 (export PDF),
                   #7 (JWT auth), #8 (historial persistente)
Próximo issue a atacar: #6 o #7 (sin dependencia bloqueante entre ellos)
```

---

## Registro de degradación de contexto detectada

| Sesión | Señal de ruido | Acción tomada |
|---|---|---|
| Handoff #1 | Agente sugirió mezclar lógica de auth en `main.py` | Handoff ejecutado, contexto reiniciado |
| Handoff #2 | Agente propuso CSS inline en `app.js` | Handoff ejecutado, separación de capas reforzada |
