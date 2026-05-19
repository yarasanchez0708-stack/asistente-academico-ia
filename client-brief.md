Perfecto! Ahora el client-brief.md. Copia este contenido:

markdown# Client Brief — Asistente Académico Inteligente

## Contexto del cliente

**Cliente:** Yara Sánchez, estudiante de desarrollo de software  
**Fecha:** Mayo 2026  
**Tipo de proyecto:** Proyecto Integrador — semestre completo

---

## El problema

Los estudiantes universitarios manejan múltiples materias simultáneamente, cada una con fechas de entrega, parciales y proyectos. La información está dispersa entre WhatsApp, calendarios, notas sueltas y correo. Esto genera:

- Tareas olvidadas o entregadas tarde
- Dificultad para priorizar qué estudiar primero
- Pérdida de tiempo buscando información académica que ya se explicó en clase

---

## Objetivo

Construir una aplicación web que centralice la gestión de tareas académicas y ofrezca un asistente IA para resolver dudas de estudio, todo en un solo lugar accesible desde el navegador.

---

## Usuarios objetivo

Estudiantes universitarios de carreras de tecnología que:
- Manejan 4–6 materias por semestre
- Prefieren herramientas web simples sobre apps móviles complejas
- Ya usan GitHub y herramientas de desarrollo

---

## Funcionalidades esperadas

### MVP (entrega inicial)
- Crear, listar y marcar como completadas tareas académicas
- Cada tarea tiene: título, materia, fecha de entrega, prioridad
- Interfaz simple y funcional

### Fase 2 (próximas entregas)
- Integración con Claude via API para responder preguntas académicas
- Sugerencia automática de prioridad según fecha de entrega
- Filtrado por materia

### Fase 3 (semestre completo)
- Autenticación de usuarios
- Historial de conversaciones con el asistente IA
- Exportar tareas a calendario

---

## Criterios de éxito

1. El backend responde correctamente en todos los endpoints documentados
2. El frontend permite crear y visualizar tareas sin errores
3. La aplicación corre localmente con instrucciones claras en el README
4. El código está organizado, comentado y versionado en GitHub

---

## Stack técnico elegido

- **Backend:** Python + FastAPI
- **Frontend:** HTML/CSS/JS vanilla
- **IA:** Anthropic API con modelo Claude
- **Dev tool principal:** Claude Code, siguiendo el flujo AFK Agent

---

## Flujo de desarrollo

Se sigue el flujo descrito en [Running Your AFK Agent](https://www.aihero.dev/running-your-afk-agent-a9l1u):

1. Se redacta este brief como contexto de referencia
2. Cada funcionalidad se convierte en un GitHub Issue detallado
3. Claude Code recibe el issue y trabaja de forma autónoma (sesión AFK)
4. Se revisa el resultado, se ajusta y se hace commit
5. Se repite por issue hasta completar el sprint

---

## Restricciones

- Sin base de datos en fase inicial (datos en memoria)
- Sin deployment en esta entrega (local únicamente)
- Tiempo de desarrollo: sesiones de 1–2 horas con Claude Code
