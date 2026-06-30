from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import List

app = FastAPI(title="Task Management API", version="1.0.0")

#---------------------------------------------------------------
# Modelos Pydantic
class TaskCreate(BaseModel):
    titulo: str = Field(min_length=1, description="Título de la task")
    contenido: str = Field(min_length=1, description="Contenido de la task")
    deadline: date = Field(description="Fecha de vencimiento")

class TaskUpdate(BaseModel):
    completada: bool = Field(description="Estado de completado")

class TaskResponse(BaseModel):
    id: int
    titulo: str
    contenido: str
    deadline: date
    completada: bool
    fecha_creacion: datetime
    
#---------------------------------------------------------------    
# Implementar clase TaskManager con lógica de negocio
class TaskManager:
    def __init__(self):
        self._tasks = {}
        self._task_counter = 0

    # FUNCION PARA CREAR UNA NUEVA TAREA
    def create_task(self, task_input: TaskCreate) -> dict:
        # Evita fechas de vencimiento en el pasado
        if task_input.deadline < date.today():
            raise ValueError("La fecha de vencimiento no puede ser en el pasado.")

        # Limpia espacios en blanco al inicio y final de los campos titulo y contenido
        formatted_title = task_input.titulo.strip().capitalize()
        formatted_content = task_input.contenido.strip()

        # Incrementar el contador interno para simular un ID Autoincremental
        self._task_counter += 1

        # Crea la task con los datos proporcionados y el ID generado
        new_task = {
            "id": self._task_counter,
            "titulo": formatted_title,
            "contenido": formatted_content,
            "deadline": task_input.deadline,
            "completada": False,
            "fecha_creacion": datetime.now()
        }

        # Persistencia en memoria local de la instancia
        self._tasks[self._task_counter] = new_task

        return new_task

    # FUNCION PARA OBTENER UNA TAREA POR ID
    def get_task_by_id(self, task_input_id: int):
        task = self._tasks.get(task_input_id)

        if not task:
            raise ValueError(f"Tarea con ID {task_input_id} no encontrada.")

        return task

    # FUNCION PARA MARCAR UNA TAREA COMO COMPLETADA
    def mark_task_completed(self, task_input_id: int):
        task = self._tasks.get(task_input_id)

        if not task:
            raise ValueError(f"Tarea con ID {task_input_id} no encontrada.")

        task["completada"] = True

        return task

    # FUNCION PARA OBTENER LAS TAREAS CADUCADAS
    def get_expired_tasks(self) -> List[dict]:
        expired_tasks = []
        today = date.today()

        for task in self._tasks.values():
            if task["deadline"] < today and not task["completada"]:
                expired_tasks.append(task)

        # Devuelve una lista de diccionarios de las tareas caducadas
        return expired_tasks

#---------------------------------------------------------------
# Se crea una sola instancia para manejar todas los endpoints de la API
task_manager = TaskManager()

#---------------------------------------------------------------
# Implementar endpoints

@app.post("/tasks/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def crear_tarea(task: TaskCreate):
    try:
        # Llamamos al cerebro para que aplique la lógica y guarde la tarea
        new_task = task_manager.create_task(task)
        return new_task
    except ValueError as e:
        # Si la fecha era del pasado, el cerebro lanzo ValueError y lo traducimos a un error web 400
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/tasks/caducadas", response_model=List[TaskResponse])
def obtener_tareas_caducadas():  
    expired_tasks = task_manager.get_expired_tasks()
    return expired_tasks

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def obtener_tarea(task_id: int):
    try:
        task = task_manager.get_task_by_id(task_id)
        return task
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@app.put("/tasks/{task_id}/completar", response_model=TaskResponse)
def marcar_completada(task_id: int):
    try:
        updated_task = task_manager.mark_task_completed(task_id)
        return updated_task
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@app.get("/")
def root():
    return {"message": "Task Management API"}