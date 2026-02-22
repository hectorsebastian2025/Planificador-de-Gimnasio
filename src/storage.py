import json
import os
from models import Recurso, Personal
from datetime import datetime, timedelta

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
            máx_clientes = p["máx_clientes"],
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
            ocupación_actual = r["ocupación_actual"]
        )
        recursos_obj.append(recursos)

    return personal_obj, recursos_obj


def contar_clientes():
    '''Cuenta el número de clientes registrados'''
    datos = cargar_datos()
    cantidad = 0
    for c in datos["gimnasio"]["clientes"]:
        if c["estado"] == "ACTIVO":
            cantidad += 1
    return cantidad

def mostrar_capacidad_rec_actual():
    '''Muestra la capacidad actual de cada recurso'''
    datos = cargar_datos()
    recursos = datos["gimnasio"]["recursos"]
    reservas = datos["gimnasio"].get("reservas", [])
    capacidad_actual = {}

    for r in recursos:
        ocupacion = 0
        for res in reservas:
            if (
                res["estado"] == "EN_CURSO" and
                res["recurso_id"] == r["id"]
            ):
                ocupacion += 1
        capacidad_actual[r["nombre"]] = f"{ocupacion}/{r['capacidad']}"

    return capacidad_actual

#-----------------------------------------------------------------------------------------------------------------------------

def actualizar_estado(datos):
    ahora = datetime.now()
    reservas = datos["gimnasio"].get("reservas", [])

    for r in reservas:
        if r["estado"] in ("CANCELADA", "FINALIZADA"):
            continue
        hora_inicio = r["turno"].split("-")[0]
        hora_fin = r["turno"].split("-")[1]

        inicio = datetime.strptime(f"{r['fecha']} {hora_inicio}", "%Y-%m-%d %H:%M")
        fin = datetime.strptime(f"{r['fecha']} {hora_fin}", "%Y-%m-%d %H:%M")

        if inicio <= ahora < fin:
            r["estado"] = "EN_CURSO"
        elif ahora >= fin:
            r["estado"] = "FINALIZADA"
