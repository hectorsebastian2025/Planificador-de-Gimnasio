import json
import os
from models import Cliente
from storage import cargar_datos, guardar_datos

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

#----------------------------------------------------------------------------------------------------------------------------

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