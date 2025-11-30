class Cliente:
    def __init__(self, nombre, id, edad, plan):
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.plan = plan

    def __repr__(self):
        return f"Cliente(id={self.id}, nombre='{self.nombre}', plan='{self.plan}')"

class Recurso:
    def __init__(self, id, tipo, nombre, capacidad, tiempo_estancia_horas, ocupación_actual):
        self.id = id
        self.tipo = tipo
        self.nombre = nombre
        self.capacidad = capacidad
        self.tiempo_estancia_horas = tiempo_estancia_horas
        self.ocupación_actual = ocupación_actual

    def __repr__(self):
        return f"Recurso(id={self.id}, nombre='{self.nombre}', ocupación_actual={self.ocupación_actual}/{self.capacidad})"

class Personal:
    def __init__(self, id, rol, máx_clientes, clientes_actuales):
        self.id = id
        self.rol = rol
        self.máx_clientes = máx_clientes
        self.clientes_actuales = clientes_actuales

    def __repr__(self):
        return f"Personal(id={self.id}, rol='{self.rol}', clientes_actuales={self.clientes_actuales}/{self.máx_clientes})"


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
    def __init__(self,capacidad_máxima, personal, recursos, planes,clientes, eventos):
        self.capacidad_maxima = capacidad_máxima
        self.personal = personal
        self.recursos = recursos
        self.planes = planes
        self.clientes = clientes
        self.eventos = eventos
    
    def __repr__(self):
        return f"Gimnasio(personal={len(self.personal)}, recursos={len(self.recursos)}, planes={len(self.planes)}, clientes={len(self.clientes)}, eventos={len(self.eventos)})"