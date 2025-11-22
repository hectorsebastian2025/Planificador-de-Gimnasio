import json
import os
from models import Cliente, Recurso, Personal, Plan, Evento

# Esto es la ruta de de este archivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Queremos ir a la carpeta data que está un nivel arriba
RUTA_DATOS = os.path.join(BASE_DIR, "..", "data", "data.json")

# Normaliza la ruta
RUTA_DATOS = os.path.normpath(RUTA_DATOS)

def cargar_datos():
    '''Carga los datos del json'''
    with open(RUTA_DATOS, "r", encoding="utf-8") as archivo:
        return json.load(archivo)
    
print("RUTA:", RUTA_DATOS)
print("Existe:", os.path.exists(RUTA_DATOS))

def guardar_datos(datos):
    '''Guarda los datos en el json'''
    with open(RUTA_DATOS, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

def cargar_objetos():
    '''Transforma los archivos del json en objetos de las clases'''
    datos = cargar_datos()
    gym = datos["gimnasio"]
    personal_obj = []

    for p in gym["personal"]:
        personal = Personal(
            id = p["id"],
            rol = p["rol"],
            max_clientes = p["max_clientes"],
            clientes_actuales = p["clientes_actuales"]
        )
        personal_obj.append(personal)

    recursos_obj = []
    for r in gym["recursos"]:
        recursos = Recurso(
            id = r["id"],
            tipo = r["tipo"],
            nombre = r["nombre"],
            capacidad = r["capacidad"],
            tiempo_estancia_horas = r["tiempo_estancia_horas"],
            ocupacion_actual = r["ocupacion_actual"]
        )
        recursos_obj.append(recursos)

    return personal_obj, recursos_obj

print(cargar_objetos())