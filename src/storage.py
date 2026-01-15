import json
import os
from models import Cliente, Recurso, Personal
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
    return len(datos["gimnasio"]["clientes"])

def capacidad_gimnasio():
    '''Devuelve la capacidad máxima del gimnasio'''
    datos = cargar_datos()
    return datos["gimnasio"]["capacidad_máxima"]

print("Número de clientes:", contar_clientes())
print("Capacidad del gimnasio:", capacidad_gimnasio())

#-----------------------------------------------------------------------------------------------------------------------------

def agregar_cliente(cliente: Cliente):
    """Agrega un nuevo cliente al gimnasio si hay capacidad."""
    
    datos = cargar_datos()
    clientes = datos["gimnasio"]["clientes"]
    capacidad = datos["gimnasio"]["capacidad_máxima"]

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
        "plan": cliente.plan,
        "estado": "ACTIVO"
    }

    clientes.append(cliente_dict)
    guardar_datos(datos)

#-----------------------------------------------------------------------------------------------------------------------------

def eliminar_cliente(cliente_id: int):
    """Elimina un cliente del gimnasio por su ID y finaliza sus reservas activas."""
    
    datos = cargar_datos()
    clientes = datos["gimnasio"]["clientes"]
    reservas = datos["gimnasio"].get("reservas", [])

    # Buscar y eliminar el cliente
    cliente_encontrado = False
    for c in clientes:
        if c["id"] == cliente_id:
            c["estado"] = "INACTIVO"
            cliente_encontrado = True
            # Finalizar reservas activas del cliente
            for r in reservas:
                if r["cliente_id"] == cliente_id and r["estado"] == "ACTIVA":
                    r["estado"] = "CANCELADA"
            break
    if not cliente_encontrado:
        raise Exception("No se encontró un cliente con ese ID.")

    guardar_datos(datos)
    return f"Cliente con ID {cliente_id} eliminado y sus reservas activas finalizadas."


#-----------------------------------------------------------------------------------------------------------------------------

def reservar_recurso(cliente_id: int, recurso_id: int, fecha_evento: str, turno: str):
    """Reserva un recurso para un cliente en una fecha y turno específicos."""

    datos = cargar_datos()
    clientes = datos["gimnasio"]["clientes"]
    recursos = datos["gimnasio"]["recursos"]
    turnos_disponibles = datos["gimnasio"]["horario"]["turnos"]

    # Buscar cliente
    cliente = None
    for c in clientes:
        if c["id"] == cliente_id and c["estado"] == "ACTIVO":
            cliente = c
            break
    if cliente is None:
        raise Exception("Cliente no encontrado.")

    #Buscar recurso
    recurso = None
    for r in recursos:
        if r["id"] == recurso_id:
            recurso = r
            break
    if recurso is None:
        raise Exception("Recurso no encontrado.")
    
        # Validar turno
    if turno not in turnos_disponibles:
        raise Exception(f"Turno inválido. Debe ser uno de: {turnos_disponibles}")

    # Validar fecha
    try:
        datetime.strptime(fecha_evento, "%Y-%m-%d")
    except ValueError:
        raise Exception("Formato de fecha inválido. Usa 'YYYY-MM-DD'.")
    
    hora_inicio = turno.split("-")[0]

    inicio_turno = datetime.strptime(
    f"{fecha_evento} {hora_inicio}", "%Y-%m-%d %H:%M")

    ahora = datetime.now()
    if inicio_turno <= ahora:
        raise Exception("No se puede reservar un turno que ya comenzó o terminó")
    if inicio_turno > ahora + timedelta(days=7):
        raise Exception("Solo se permiten reservas hasta 7 días en el futuro.")

    # Validar plan del cliente
    plan_cliente = cliente["plan"]
    plan_obj = None
    for p in datos["gimnasio"]["planes"]:
        if p["nombre"] == plan_cliente:
            plan_obj = p
            break
    if plan_obj is None:
        raise Exception("Plan del cliente no encontrado.")

    #Validar si el cliente puede acceder a la sala de musculacion con el plan que tiene
    acceso_recurso = recurso["nombre"]
    if recurso["nombre"] == "Sala de musculación":
        if "con entrenador" in plan_cliente:
            acceso_recurso += " (con entrenador)"
        else:
            acceso_recurso += " (sin entrenador)"

    # Validar si puede acceder al recurso segun el plan que tiene
    if acceso_recurso not in plan_obj["acceso"]:
        raise Exception(f"El cliente no puede acceder a '{acceso_recurso}' con su plan '{plan_cliente}'.")

    # Crear lista de reservas si no existe
    reservas = datos["gimnasio"].setdefault("reservas", [])

    # Validar que el cliente no tenga otra reserva en ese turno
    for r in reservas:
        if (
            r["estado"] == "ACTIVA" and
            r["cliente_id"] == cliente_id and 
            r["fecha"] == fecha_evento and 
            r["turno"] == turno
        ):
            raise Exception("El cliente ya tiene una reserva en ese turno.")

    # Validar capacidad del recurso en ese turno
    ocupacion = 0
    for r in reservas:
        if (
            r["estado"] == "ACTIVA" and
            r["recurso_id"] == recurso_id and 
            r["fecha"] == fecha_evento and 
            r["turno"] == turno
        ):
            ocupacion += 1
    if ocupacion >= recurso["capacidad"]:
        raise Exception("Recurso no disponible: capacidad máxima alcanzada en ese turno.")
    
    nuevo_id = 1
    if len(reservas) > 0:
        nuevo_id = reservas[-1]["id"] + 1

    neces_personal = False
    rol_necesario = None
    for e in datos["gimnasio"]["MAPA_DE_ROLES"].keys():
        if e == recurso["nombre"]:
            neces_personal = True
            rol_necesario = datos["gimnasio"]["MAPA_DE_ROLES"][e]
            break

    personal_disponible = True
    if neces_personal:
        for p in reservas:
            if (
                p["estado"] == "ACTIVA" and
                p.get("personal_necesario") == rol_necesario and 
                p["fecha"] == fecha_evento and 
                p["turno"] == turno
            ):
                personal_disponible = False
                break
        if not personal_disponible:
            raise Exception(f"No hay personal disponible con el rol '{rol_necesario}' para asistir al cliente.")
    


    # Registrar la reserva
    reserva = {
        "id": nuevo_id,
        "cliente_id": cliente_id,
        "recurso_id": recurso_id,
        "fecha": fecha_evento,
        "turno": turno,
        "estado": "ACTIVA"
    }
    if personal_disponible:
        reserva["personal_necesario"] = rol_necesario
    reservas.append(reserva)
    guardar_datos(datos)

    return f"Reserva exitosa para {cliente['nombre']} en {recurso['nombre']} el {fecha_evento} en el turno {turno}."

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

#-----------------------------------------------------------------------------------------------------------------------------

def eliminar_reserva(cliente_id: int, recurso_id: int, fecha_evento: str, turno: str, reserva_id: int):
    datos = cargar_datos()
    clientes = datos["gimnasio"]["clientes"]
    reservas = datos["gimnasio"]["reservas"]
    recursos = datos["recursos"]
    turnos_disponibles = datos["gimnasio"]["horario"]["turnos"]

    # Buscar cliente
    cliente = None
    for c in clientes:
        if c["id"] == cliente_id and c["estado"] == "ACTIVO":
            cliente = c
            break
    if cliente is None:
        raise Exception("Cliente no encontrado.")

    #Buscar recurso
    recurso = None
    for r in recursos:
        if r["id"] == recurso_id:
            recurso = r
            break
    if recurso is None:
        raise Exception("Recurso no encontrado.")

    # Validar fecha
    try:
        datetime.strptime(fecha_evento, "%Y-%m-%d")
    except ValueError:
        raise Exception("Formato de fecha inválido. Usa 'YYYY-MM-DD'.")
    
    # Validar turno
    if turno not in turnos_disponibles:
        raise Exception(f"Turno inválido. Debe ser uno de: {turnos_disponibles}")

    # Validar que existe el turno a eliminar
    for r in reservas:
        if (
            r["id"] == reserva_id and
            r["cliente_id"] == cliente_id and 
            r["recurso_id"] == recurso_id and 
            r["fecha"] == fecha_evento and 
            r["turno"] == turno
        ):
            if r["estado"] == "CANCELADA":
                raise Exception("La reserva ya está cancelada.")
            r["estado"] = "CANCELADA"
            guardar_datos(datos)
            return f"Reserva cancelada para {cliente['nombre']} en {recurso['nombre']} el {fecha_evento} en el turno {turno}."
        

#---------------------------------------------------------------------------------------------------------------------------

def cancelar_reserva(reserva_id: int):
    '''Cancela la reserva segun el id de la reserva'''
    
    datos = cargar_datos()
    reservas = datos["gimnasio"]["reservas"]

    for r in reservas:
        if r["id"] == reserva_id:
            if r["estado"] != "ACTIVA":
                raise Exception("Solo se pueden cancelar reservas activas.")

            r["estado"] = "CANCELADO"

        guardar_datos(datos)
        return f"Reserva con ID {reserva_id} cancelada."
    
    raise Exception("No se encontró una reserva con ese ID.")

#---------------------------------------------------------------------------------------------------------------------------

def alternativa_reservar_recurso(cliente_id: int, recurso_id: int, fecha_evento: str, turno: str):
    """Busca alternativas de reserva cuando no hay disponibilidad"""

    datos = cargar_datos()
    reservas = datos["gimnasio"].get("reservas", [])
    recursos = datos["gimnasio"]["recursos"]
    turnos_disponibles = datos["gimnasio"]["horario"]["turnos"]

    # Buscar recurso
    recurso = None
    for r in recursos:
        if r["id"] == recurso_id:
            recurso = r
            break

    if recurso is None:
        raise Exception("Recurso no encontrado")

    fecha_base = datetime.strptime(fecha_evento, "%Y-%m-%d")
    hoy = datetime.now()
    fecha_max = hoy + timedelta(days=7)

    alternativas = []
    MAX_ALTERNATIVAS = 3

    dias = 0
    while dias <= 7 and len(alternativas) < MAX_ALTERNATIVAS:
        fecha_eval = fecha_base + timedelta(days=dias)
        fecha_str = fecha_eval.strftime("%Y-%m-%d")

        if fecha_eval > fecha_max:
            break

        for t in turnos_disponibles:
            if t == turno and dias == 0:
                continue

            # Validar que el turno no esté en el pasado
            hora_inicio = t.split("-")[0]
            inicio_turno = datetime.strptime(
                f"{fecha_str} {hora_inicio}", "%Y-%m-%d %H:%M"
            )

            if inicio_turno <= hoy:
                continue

            # Validar que el cliente no tenga reserva en ese turno
            conflicto_cliente = False
            for r in reservas:
                if (
                    r["estado"] == "ACTIVA" and
                    r["cliente_id"] == cliente_id and
                    r["fecha"] == fecha_str and
                    r["turno"] == t
                ):
                    conflicto_cliente = True
                    break

            if conflicto_cliente:
                continue

            # Calcular ocupación del recurso
            ocupacion = 0
            for r in reservas:
                if (
                    r["estado"] == "ACTIVA" and
                    r["recurso_id"] == recurso_id and
                    r["fecha"] == fecha_str and
                    r["turno"] == t
                ):
                    ocupacion += 1

            if ocupacion < recurso["capacidad"]:
                alternativas.append((fecha_str, t))

            if len(alternativas) >= MAX_ALTERNATIVAS:
                break

        dias += 1

    return alternativas




