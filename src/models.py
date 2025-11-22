class Cliente:
    def __init__(self, nombre, edad, plan, turno):
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.plan = plan
        self.turno = turno

    def __repr__(self):
        return f"Cliente(id={self.id}, nombre='{self.nombre}', plan='{self.plan}', turno='{self.turno}')"

class Recurso:
    def __init__(self, id, tipo, nombre, capacidad, tiempo_estancia_horas, ocupacion_actual):
        self.id = id
        self.tipo = tipo
        self.nombre = nombre
        self.capacidad = capacidad
        self.tiempo_estancia_horas = tiempo_estancia_horas
        self.ocupacion_actual = ocupacion_actual

    def __repr__(self):
        return f"Recurso(id={self.id}, nombre='{self.nombre}', ocupacion_actual={self.ocupacion_actual}/{self.capacidad})"

class Personal:
    def __init__(self, id, rol, max_clientes, clientes_actuales):
        self.id = id
        self.rol = rol
        self.max_clientes = max_clientes
        self.clientes_actuales = clientes_actuales

    def __repr__(self):
        return f"Personal(id={self.id}, rol='{self.rol}', clientes_actuales={self.clientes_actuales}/{self.max_clientes})"


class Plan:
    def __init__(self, nombre, precio_mensual, acceso):
        self.nombre = nombre
        self.precio_mensual = precio_mensual
        self.acceso = acceso

    def __repr__(self):
        return f"Plan(nombre='{self.nombre}', precio={self.precio_mensual}, acceso={self.acceso})"

class Evento:
    def __init__(self, id, nombre, turno, recursos_asignados, personal_asignado):
        self.id = id
        self.nombre = nombre
        self.turno = turno
        self.recursos_asignados = recursos_asignados
        self.personal_asignado = personal_asignado

    def __repr__(self):
        recursos = []
        for r in self.recursos_asignados:
            recursos.append(r.nombre)
        personal = []
        for p in self.personal_asignado:
            personal.append(p.rol)
        return f"Evento(id={self.id}, nombre='{self.nombre}', turno='{self.turno}', recursos={recursos}, personal={personal})"
        
class Gimnasio:
    def __init__(self,capacidad_maxima, personal, recursos, planes,clientes, eventos):
        self.capacidad_maxima = capacidad_maxima
        self.personal = personal
        self.recursos = recursos
        self.planes = planes
        self.clientes = clientes
        self.eventos = eventos
    
    def __repr__(self):
        return f"Gimnasio(personal={len(self.personal)}, recursos={len(self.recursos)}, planes={len(self.planes)}, clientes={len(self.clientes)}, eventos={len(self.eventos)})"