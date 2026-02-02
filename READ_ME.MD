Bienvenido a Code Fit Gym

El gimnasio de Code Fit Gym está compuesto por un equipo magnífico de entrenadores, fisioterapeutas, médicos del deporte y nutricionistas que te ayudarán a alcanzar tu mejor versión.

El centro está equipado con máquinas de alta tecnología que tienen cierta capacidad:


Sala de musculación       Capacidad: 40
Cancha de básket          Capacidad: 15
Cancha de fútbol          Capacidad: 25
Piscina semiolímpica      Capacidad: 12
Sauna                     Capacidad: 15
Sala de fisioterapia      Capacidad: 2
Jacuzzi                   Capacidad: 10
Consultorio médico        Capacidad: 2
Cámara hiperbárica        Capacidad: 2
Nutricionista             Capacidad: 2

Existen tres niveles de acceso a los recursos:

Plan Básico que cuenta con acceso a:

"Sala de musculación (sin entrenador)",
"Cancha de básket",
"Cancha de fútbol",
"Piscina semiolímpica",
"Sauna"

Plan Básico con entrendaor que cuenta con acceso a:

"Sala de musculación (con entrenador)",
"Cancha de básket",
"Cancha de fútbol",
"Piscina semiolímpica",
"Sauna"

Plan Premium:

"Sala de musculación (sin entrenador)",
"Cancha de básket",
"Cancha de fútbol",
"Piscina semiolímpica",
"Sauna",
"Sala de musculación (con entrenador)",
"Sala de fisioterapia",
"Jacuzzi",
"Consultorio médico",
"Nutricionista",
"Cámara hiperbárica"

Para el disfrute de nuestras secciones en el gym se tiene en cuenta el horario, el cual está compuesto por 6 turnos:

"08:00-10:00",
"10:00-12:00",
"12:00-14:00",
"14:00-16:00",
"16:00-18:00",
"18:00-20:00"


La idea principal fue utilizar POO para los Clientes ya que es la entidad principal del sistema y el resto como las Reservas, Recursos, Planes, Personal son estructuras de apoyo que pueden evolucionar a POO en un futuro si la complejidad lo requiere.

Para la interfaz gráfica se utilizó streamlit ya que es bastante intuitiva y relativamente fácil de manejar.

Para registrar cliente se verifica si existe capacidad en el centro para su registro. Cuando el cliente queda registrado se le asigna un ID único.

La capcidad total del gimnasio es de 700 personas:

Restricción: Si la capcaidad del gimnasio es máxima no se puede registrar al cliente

La reserva de un recurso se puede efectuar a partir de el momento en que se está solicitando la reserva hasta 7 días en adelante:
Restricciones:
No se puede reservar en un turno que ya comenzó o terminó
Solo se permiten reservas hasta 7 días en el futuro 
Si el cliente quiere reservar un evento el cual no está disponible según el plan que adquirió se le imposibilita la reserva del recurso
Si el cliente tiene una reserva en la misma fecha/turno que quiere reservar, se le cancela la reserva
Si la capacidad del recurso en el horario que el cliente quiere hacer su reserva es máxima no puede hacer la reserva
Si el recurso que solicita necesita de personal y no está disponible, se cancela la reserva

Las reservas se pueden encontrar en 4 estados:
ACTIVA: Si la reserva se encuntra activa
EN CURSO: Si la reserva se encuentra en ejecución 
INACTIVA: Si ya pasó el tiempo de la reserva
CANCELADA: Si la reserva fue cancelada

Si el cliente decide quitarse del sistema y no asistir más al gimnasio las reservas que tenía activas van a ser canceladas

Dificultades:
A la hora de transicionar de una reserva activa a estar en curso o finalizada, para esto se implementó la función actualizar estado que se ejecuta en todas las páginas de la UI

Alternativa de recurso: en caso de que el cliente no pueda reservar un evento se le otorgan 3 fechas alternativas, para esto se implementó la función alternativa_reservar_recurso la cual toma 3 fechas: la fecha base(la fecha en que el cliente quiso reservar y no se pudo), la fecha de hoy, y 7 días en adelante, lo que se hace es coger el turno siguiente al de la reserva inválida y evaluar si se puede realizar la reserva teniendo en cuenta si el cliente ya tiene una reservación en ese turno y la ocupación del recurso, si es el caso entonces se busca para el siguiente turno etc, luego si se llegara el caso de que cae en el último turno pues se revisa a partir del primer turno del otro día si es necesario hasta completar ls tres fechas.




