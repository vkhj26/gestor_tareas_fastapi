# Task Management API

API REST para la gestión de tareas desarrollada con FastAPI.

## Descripción

**Task Management API** es una API REST construida con FastAPI que permite crear, consultar y gestionar tareas. La aplicación proporciona funcionalidades para:

- ✅ Crear nuevas tareas con título, descripción y fecha de vencimiento
- 📋 Consultar tareas individuales por ID
- ✓ Marcar tareas como completadas
- ⏰ Obtener lista de tareas con vencimiento caducado
- 📝 Validación automática de datos

## Tecnologías

- **FastAPI** - Framework web moderno y de alto rendimiento
- **Pydantic** - Validación de datos
- **Uvicorn** - Servidor ASGI
- **Python 3.7+**

## Instalación

### 1. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

Puedes usar cualquiera de estos comandos:

```bash
# Opción 1: Comando moderno de FastAPI (recomendado)
fastapi dev main.py

# Opción 2: Uvicorn tradicional
uvicorn main:app --reload
```

La API estará disponible en `http://localhost:8000`

### Documentación interactiva

Una vez que la aplicación esté corriendo, accede a:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Modelos de Datos

### TaskCreate (Request)
Modelo para crear una nueva tarea:

```json
{
  "titulo": "string (requerido, mínimo 1 carácter)",
  "contenido": "string (requerido, mínimo 1 carácter)",
  "deadline": "date (YYYY-MM-DD, no puede ser en el pasado)"
}
```

### TaskUpdate (Request)
Modelo para actualizar el estado de una tarea:

```json
{
  "completada": "boolean"
}
```

### TaskResponse (Response)
Respuesta de la API con los datos completos de una tarea:

```json
{
  "id": "integer",
  "titulo": "string",
  "contenido": "string",
  "deadline": "date",
  "completada": "boolean",
  "fecha_creacion": "datetime"
}
```

## Endpoints

### 1. Información de la API
```
GET /
```
**Descripción:** Obtiene información básica de la API

**Respuesta (200):**
```json
{
  "message": "Task Management API"
}
```

---

### 2. Crear una nueva tarea
```
POST /tasks/
```
**Descripción:** Crea una nueva tarea

**Request Body:**
```json
{
  "titulo": "Completar proyecto",
  "contenido": "Terminar el desarrollo de la API de tareas",
  "deadline": "2026-12-31"
}
```

**Respuesta (201):**
```json
{
  "id": 1,
  "titulo": "Completar proyecto",
  "contenido": "Terminar el desarrollo de la API de tareas",
  "deadline": "2026-12-31",
  "completada": false,
  "fecha_creacion": "2026-06-30T10:30:45.123456"
}
```

**Errores:**
- `400 Bad Request` - Si la fecha de vencimiento es en el pasado
- `422 Unprocessable Entity` - Si faltan campos requeridos o son inválidos

---

### 3. Obtener una tarea por ID
```
GET /tasks/{task_id}
```
**Descripción:** Obtiene los detalles de una tarea específica

**Parámetros:**
- `task_id` (path, requerido): ID de la tarea

**Respuesta (200):**
```json
{
  "id": 1,
  "titulo": "Completar proyecto",
  "contenido": "Terminar el desarrollo de la API de tareas",
  "deadline": "2026-12-31",
  "completada": false,
  "fecha_creacion": "2026-06-30T10:30:45.123456"
}
```

**Errores:**
- `404 Not Found` - Si la tarea no existe

---

### 4. Marcar una tarea como completada
```
PUT /tasks/{task_id}/completar
```
**Descripción:** Marca una tarea como completada

**Parámetros:**
- `task_id` (path, requerido): ID de la tarea

**Respuesta (200):**
```json
{
  "id": 1,
  "titulo": "Completar proyecto",
  "contenido": "Terminar el desarrollo de la API de tareas",
  "deadline": "2026-12-31",
  "completada": true,
  "fecha_creacion": "2026-06-30T10:30:45.123456"
}
```

**Errores:**
- `404 Not Found` - Si la tarea no existe

---

### 5. Obtener tareas caducadas
```
GET /tasks/caducadas
```
**Descripción:** Obtiene la lista de tareas cuya fecha de vencimiento ha pasado y aún no están completadas

**Respuesta (200):**
```json
[
  {
    "id": 1,
    "titulo": "Tarea antigua",
    "contenido": "Una tarea con vencimiento pasado",
    "deadline": "2025-12-31",
    "completada": false,
    "fecha_creacion": "2025-06-30T10:30:45.123456"
  }
]
```

## Ejemplos de Uso

### Con cURL

```bash
# Crear una tarea
curl -X POST "http://localhost:8000/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Estudiar FastAPI",
    "contenido": "Aprender FastAPI y sus conceptos clave",
    "deadline": "2026-12-31"
  }'

# Obtener una tarea
curl -X GET "http://localhost:8000/tasks/1"

# Marcar como completada
curl -X PUT "http://localhost:8000/tasks/1/completar"

# Obtener tareas caducadas
curl -X GET "http://localhost:8000/tasks/caducadas"
```

### Con Python (requests)

```python
import requests
from datetime import date, timedelta

BASE_URL = "http://localhost:8000"

# Crear una tarea
task_data = {
    "titulo": "Estudiar FastAPI",
    "contenido": "Aprender FastAPI y sus conceptos clave",
    "deadline": str(date.today() + timedelta(days=30))
}
response = requests.post(f"{BASE_URL}/tasks/", json=task_data)
print(response.json())

# Obtener una tarea
response = requests.get(f"{BASE_URL}/tasks/1")
print(response.json())

# Marcar como completada
response = requests.put(f"{BASE_URL}/tasks/1/completar")
print(response.json())

# Obtener tareas caducadas
response = requests.get(f"{BASE_URL}/tasks/caducadas")
print(response.json())
```

## Ejecutar Tests

Para ejecutar los tests de la API:

```bash
python test_api.py
```

Los tests validan:
- Creación correcta de tareas
- Validación de fechas en el pasado
- Obtención de tareas por ID
- Actualización de estado (completada)
- Obtención de tareas caducadas
- Manejo de errores 404

## Características de Validación

- **Título y contenido:** Deben tener al menos 1 carácter
- **Fecha de vencimiento:** No puede ser en el pasado
- **Formato de fecha:** YYYY-MM-DD
- **Capitalización:** El título se capitaliza automáticamente
- **Espacios en blanco:** Se eliminan automáticamente del título y contenido

## Almacenamiento

Actualmente, la aplicación almacena las tareas en memoria. Esto significa que:
- ✅ Los datos se pierden al reiniciar la aplicación
- 📝 Es ideal para desarrollo y testing
- 💾 Para producción, se recomienda integrar una base de datos (PostgreSQL, MongoDB, etc.)

## Futuras Mejoras

- [ ] Persistencia en base de datos
- [ ] Autenticación y autorización
- [ ] Filtros avanzados por estado y fecha
- [ ] Paginación de resultados
- [ ] Etiquetas/categorías de tareas
- [ ] Prioridades de tareas

## Licencia

Este proyecto es parte del curso de Programación Avanzada.

```bash
python test_api.py
```

## Documentación interactiva

Una vez ejecutando la aplicación, puedes acceder a:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
