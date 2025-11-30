import json
import os
from models import Cliente, Recurso, Personal, Plan, Evento
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

def contar_clientes():
    '''Cuenta el número de clientes registrados'''
    datos = cargar_datos()
    return len(datos["gimnasio"]["clientes"])

def capacidad_gimnasio():
    '''Devuelve la capacidad máxima del gimnasio'''
    datos = cargar_datos()
    return datos["gimnasio"]["capacidad_maxima"]

print("Número de clientes:", contar_clientes())
print("Capacidad del gimnasio:", capacidad_gimnasio())

def agregar_cliente(cliente: Cliente):
    """Agrega un nuevo cliente al gimnasio si hay capacidad."""
    
    datos = cargar_datos()
    
    clientes = datos["gimnasio"]["clientes"]
    capacidad = datos["gimnasio"]["capacidad_maxima"]

    # Validar capacidad
    if len(clientes) >= capacidad:
        raise Exception("Capacidad máxima del gimnasio alcanzada.")

    # Validar ID repetido
    for c in clientes:
        if c["id"] == cliente.id:
            raise Exception("Ya existe un cliente con ese ID.")
    
    # Registrar el cliente
    cliente_dict = {
        "id": cliente.id,
        "nombre": cliente.nombre,
        "edad": cliente.edad,
        "plan": cliente.plan
    }

    clientes.append(cliente_dict)
    guardar_datos(datos)

'''
def eliminar_cliente(cliente_id: int):
    """Elimina un cliente del gimnasio por su ID."""
    
    datos = cargar_datos()
    clientes = datos["gimnasio"]["clientes"]

    # Buscar y eliminar el cliente
    cliente_encontrado = False
    for i, c in enumerate(clientes):
        if c["id"] == cliente_id:
            del clientes[i]
            cliente_encontrado = True
            break

    if not cliente_encontrado:
        raise Exception("No se encontró un cliente con ese ID.")

    guardar_datos(datos)
    '''

def reservar_recurso(cliente_id: int, recurso_id: int, fecha_evento: str, turno: str):
    """Reserva un recurso para un cliente en una fecha y turno específicos."""

    datos = cargar_datos()
    clientes = datos["gimnasio"]["clientes"]
    recursos = datos["gimnasio"]["recursos"]
    turnos_disponibles = datos["gimnasio"]["horario"]["turnos"]

    # --- 1. Buscar cliente ---
    cliente = None
    for c in clientes:
        if c["id"] == cliente_id:
            cliente = c
            break
    if cliente is None:
        raise Exception("Cliente no encontrado.")

    # --- 2. Buscar recurso ---
    recurso = None
    for r in recursos:
        if r["id"] == recurso_id:
            recurso = r
            break
    if recurso is None:
        raise Exception("Recurso no encontrado.")

    # --- 3. Validar fecha ---
    try:
        fecha_dt = datetime.strptime(fecha_evento, "%Y-%m-%d")
    except ValueError:
        raise Exception("Formato de fecha inválido. Usa 'YYYY-MM-DD'.")
    
    hoy = datetime.now()
    if fecha_dt < hoy:
        raise Exception("No se pueden reservar fechas pasadas.")
    if fecha_dt > hoy + timedelta(days=30):
        raise Exception("Solo se permiten reservas hasta 30 días en el futuro.")

    # --- 4. Validar turno ---
    if turno not in turnos_disponibles:
        raise Exception(f"Turno inválido. Debe ser uno de: {turnos_disponibles}")

    # --- 5. Validar plan del cliente ---
    plan_cliente = cliente["plan"]
    plan_obj = None
    for p in datos["gimnasio"]["planes"]:
        if p["nombre"] == plan_cliente:
            plan_obj = p
            break
    if plan_obj is None:
        raise Exception("Plan del cliente no encontrado.")

    acceso_recurso = recurso["nombre"]
    if acceso_recurso not in plan_obj["acceso"]:
        raise Exception(f"El cliente no puede acceder a '{acceso_recurso}' con su plan '{plan_cliente}'.")

    # --- 6. Crear lista de reservas si no existe ---
    reservas = datos["gimnasio"].setdefault("reservas", [])

    # --- 7. Validar que el cliente no tenga otra reserva en ese turno ---
    for r in reservas:
        if r["cliente_id"] == cliente_id and r["fecha"] == fecha_evento and r["turno"] == turno:
            raise Exception("El cliente ya tiene una reserva en ese turno.")

    # --- 8. Validar capacidad del recurso en ese turno ---
    ocupacion = 0
    for r in reservas:
        if r["recurso_id"] == recurso_id and r["fecha"] == fecha_evento and r["turno"] == turno:
            ocupacion += 1
    if ocupacion >= recurso["capacidad"]:
        raise Exception("Recurso no disponible: capacidad máxima alcanzada en ese turno.")

    # --- 9. Registrar la reserva ---
    reserva = {
        "cliente_id": cliente_id,
        "recurso_id": recurso_id,
        "fecha": fecha_evento,
        "turno": turno
    }
    reservas.append(reserva)
    guardar_datos(datos)

    return f"Reserva exitosa para {cliente['nombre']} en {recurso['nombre']} el {fecha_evento} en el turno {turno}."
