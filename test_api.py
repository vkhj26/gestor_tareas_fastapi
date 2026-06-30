import requests
import json
from datetime import datetime, date, timedelta

BASE_URL = "http://localhost:8000"

# Variables globales para compartir ID entre los tests
tarea_valida_id = None
tarea_caducada_id = None

# Test para crear una tarea valida-------------------------------------------------------
def test_crear_tarea():
    global tarea_valida_id
    print("\n--- Test: Crear Tarea Valida ---\n")

    # Variables que guarda la fecha de hoy + 1
    fecha_valida = (date.today() + timedelta(days=1)).isoformat()
    
    # Creamos el paqete de datos para enviar al endpoint
    payload = {
        "titulo": "  aprender testing con python  ", # Ponemos espacios y minúsculas para verificar que main.py limpia el texto
        "contenido": "  crear scripts con la libreria requests  ",
        "deadline": fecha_valida
    }
    
    # Enviamos la solicitud POST al endpoint /tasks/
    response = requests.post(f"{BASE_URL}/tasks/", json=payload)
    
    # Si el status code es 201, significa que la tarea fue creada exitosamente
    print(f"Status Code esperado: 201 | Obtenido: {response.status_code}")
    assert response.status_code == 201, "Error al crear la tarea"
    
    # Obtenemos la respuesta en formato JSON y guardamos el ID de la tarea creada
    data = response.json()
    #   data = {
    #       "id": 1,
    #       "titulo": "Aprender testing con python",
    #       "completada": False
    #   }

    tarea_valida_id = data["id"]
    
    print(f"Tarea creada exitosamente con ID: {tarea_valida_id}")
    print(f"Título formateado por el backend: '{data['titulo']}'")
    print(f"Contenido formateado por el backend: '{data['contenido']}'")
    assert data["titulo"] == "Aprender testing con python" # Verifica el .strip().capitalize()
    assert data["contenido"] == "crear scripts con la libreria requests" # Verifica el .strip()

# Test para crear una tarea con fecha pasada (debe fallar)-------------------------------------------------------
def test_datos_incorrectos():
    print("\n--- Test: Crear Tarea con Fecha Pasada (Error 400) ---\n")
    
    # Ayer
    fecha_pasada = (date.today() - timedelta(days=1)).isoformat()
    
    payload = {
        "titulo": "Tarea del pasado",
        "contenido": "Esto deberia fallar.",
        "deadline": fecha_pasada
    }
    
    response = requests.post(f"{BASE_URL}/tasks/", json=payload)
    
    print(f"Status Code esperado: 400 | Obtenido: {response.status_code}")
    print(f"Respuesta del servidor: {response.json()}")
    assert response.status_code == 400, "Se esperaba un código 400 Bad Request"

# Test para obtener una tarea por ID-----------------------------------------------------------------------
def test_obtener_tarea():
    global tarea_valida_id
    print("\n--- Test: Obtener Tarea por ID ---\n")
    
    # Intentamos buscar la tarea valida creada en el primer test
    response = requests.get(f"{BASE_URL}/tasks/{tarea_valida_id}")
    
    print(f"Status Code esperado: 200 | Obtenido: {response.status_code}")
    assert response.status_code == 200, "No se pudo obtener la tarea"
    
    data = response.json()
    print(f"Datos obtenidos de la tarea {tarea_valida_id}: {data['titulo']} - Completada: {data['completada']}")
    assert data["id"] == tarea_valida_id, "El ID de la tarea obtenida no coincide con el esperado"

# Test para marcar una tarea como completada-----------------------------------------------------------------------
def test_marcar_completada():
    global tarea_valida_id
    print("\n--- Test: Marcar Tarea como Completada ---\n")
    
    response = requests.put(f"{BASE_URL}/tasks/{tarea_valida_id}/completar")
    
    print(f"Status Code esperado: 200 | Obtenido: {response.status_code}")
    assert response.status_code == 200, "Error al completar la tarea"
    
    data = response.json()
    print(f"Nuevo estado 'completada' de la tarea: {data['completada']}")
    assert data["completada"] is True, "La tarea no cambio su estado a True"

# Test para obtener tareas caducadas-----------------------------------------------------------------------
def test_obtener_tareas_caducadas():
    print("\n--- Test: Obtener Tareas Caducadas ---\n")
    
    # Como el backend no nos deja crear tareas en el pasado directamente por la API,
    # si ejecutamos este test de inmediato, la lista debería estar vacía []
    response = requests.get(f"{BASE_URL}/tasks/caducadas")
    
    print(f"Status Code esperado: 200 | Obtenido: {response.status_code}")
    assert response.status_code == 200, "Error al obtener tareas caducadas"
    
    data = response.json()
    print(f"Tareas caducadas encontradas (debe ser una lista): {data}")
    assert isinstance(data, list), "El endpoint caducadas no devolvió una lista"

# Main block para ejecutar los tests-----------------------------------------------------------------------
if __name__ == "__main__":
    print("Ejecutando tests...")
    
    try:
        test_crear_tarea()
        test_datos_incorrectos()
        test_obtener_tarea()
        test_marcar_completada()
        test_obtener_tareas_caducadas()
        
        print("\nTodos los tests pasaron exitosamente")
    except requests.exceptions.ConnectionError:
        print("\nERROR CRÍTICO: No se pudo conectar al servidor.")
    except AssertionError as e:
        print(f"\n EL TEST FALLO: {e}")
    
    print("Tests completados")
