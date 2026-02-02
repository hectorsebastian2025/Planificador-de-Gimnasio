# 🏋️‍♂️ CodeFit Gym – Sistema de Planificación y Reservas

## 📌 Descripción General
**CodeFit Gym** es un sistema de gestión y planificación de un gimnasio moderno que permite el registro de clientes, la gestión de recursos y la reserva de actividades según planes de acceso, capacidades, horarios y disponibilidad de personal especializado.

El gimnasio cuenta con un equipo multidisciplinario compuesto por entrenadores, fisioterapeutas, médicos deportivos y nutricionistas, enfocados en ayudar a los clientes a alcanzar su mejor versión.

---

## 🏢 Recursos del Gimnasio y Capacidades

| Recurso | Capacidad |
|------|----------|
| Sala de musculación | 40 |
| Cancha de básket | 15 |
| Cancha de fútbol | 25 |
| Piscina semiolímpica | 12 |
| Sauna | 15 |
| Sala de fisioterapia | 2 |
| Jacuzzi | 10 |
| Consultorio médico | 2 |
| Cámara hiperbárica | 2 |
| Nutricionista | 2 |

---

## 🎫 Planes de Acceso

### 🔹 Plan Básico
- Sala de musculación (sin entrenador)
- Cancha de básket
- Cancha de fútbol
- Piscina semiolímpica
- Sauna

### 🔹 Plan Básico con Entrenador
- Sala de musculación (con entrenador)
- Cancha de básket
- Cancha de fútbol
- Piscina semiolímpica
- Sauna

### 🔹 Plan Premium
Incluye todos los recursos anteriores, además de:
- Sala de fisioterapia
- Jacuzzi
- Consultorio médico
- Nutricionista
- Cámara hiperbárica

---

## ⏰ Horarios
El gimnasio opera en **6 turnos diarios**:

- 08:00 – 10:00  
- 10:00 – 12:00  
- 12:00 – 14:00  
- 14:00 – 16:00  
- 16:00 – 18:00  
- 18:00 – 20:00  

---

## 🧩 Decisiones de Diseño
Se utilizó **Programación Orientada a Objetos (POO)** exclusivamente para la entidad **Cliente**, ya que es la entidad principal del sistema y posee identidad y estado propios.

El resto de los componentes (Reservas, Recursos, Planes y Personal) se implementaron mediante estructuras de datos simples (diccionarios), permitiendo una evolución futura a POO si la complejidad del sistema lo requiere.

---

## 🖥️ Interfaz Gráfica
La interfaz se desarrolló con **Streamlit**, por ser una herramienta intuitiva, rápida de implementar y adecuada para prototipos funcionales.

---

## 👤 Registro de Clientes
- Cada cliente registrado recibe un **ID único**
- Capacidad total del gimnasio: **700 personas**

### Restricción
- No se permite el registro de nuevos clientes si la capacidad máxima del gimnasio ha sido alcanzada

---

## 📅 Reservas de Recursos

Las reservas pueden realizarse desde el **momento actual hasta 7 días en el futuro**.

### Restricciones:
- No se puede reservar un turno que ya comenzó o terminó
- No se permiten reservas con más de 7 días de antelación
- El cliente solo puede reservar recursos incluidos en su plan
- Un cliente no puede tener más de una reserva en el mismo turno y fecha
- No se permite reservar si la capacidad del recurso está completa
- Si el recurso requiere personal y este no está disponible, la reserva se cancela

---

## 🔄 Estados de una Reserva
- **ACTIVA**: Reserva válida
- **EN CURSO**: Reserva en ejecución
- **INACTIVA**: Reserva finalizada
- **CANCELADA**: Reserva cancelada

Si un cliente es eliminado del sistema, **todas sus reservas activas son canceladas automáticamente**.

---

## 🔁 Actualización de Estados
Para manejar correctamente la transición de estados de las reservas (activa, en curso, finalizada), se implementó una función de actualización que se ejecuta en todas las páginas de la interfaz.

---

## 🔄 Alternativas de Reserva
Si un cliente no puede reservar un recurso, el sistema ofrece **hasta 3 fechas alternativas**, evaluando:
- El turno siguiente al solicitado
- La ocupación del recurso
- Las reservas previas del cliente
- El límite de 7 días hacia adelante

Si se alcanza el último turno del día, la búsqueda continúa desde el primer turno del día siguiente hasta completar las tres alternativas.

---

## 🧪 Dificultades Encontradas
- Gestión del cambio de estado automático de las reservas
- Coordinación entre capacidad, turnos, planes y disponibilidad de personal
- Implementación de alternativas de reserva sin romper restricciones

---

## 🧠 Conclusión
Este proyecto demuestra un diseño consciente del dominio del problema, aplicando reglas de negocio reales y estructuras escalables.  
La arquitectura permite una evolución futura sin comprometer la simplicidad inicial del sistema.
