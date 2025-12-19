import streamlit as st
from datetime import date, timedelta
from storage import cargar_objetos, guardar_datos, cargar_datos, reservar_recurso, actualizar_estado

datos = cargar_datos()
actualizar_estado(datos)
guardar_datos(datos)

clientes = datos["gimnasio"]["clientes"]
recursos = datos["gimnasio"]["recursos"]
turnos = datos["gimnasio"]["horario"]["turnos"]

if len(clientes) == 0:
    st.warning("No hay clientes registrados.")
else:
    clientes_dict = {}
    for c in clientes:
        if c["estado"] == "INACTIVO":
            continue
        clave = f"{c['nombre']} (ID {c['id']})"
        valor = c["id"]
        clientes_dict[clave] = valor
    cliente_seleccionado = st.selectbox("Cliente:", list(clientes_dict.keys()))
    cliente_id = clientes_dict[cliente_seleccionado]

hoy = date.today()
limite = hoy + timedelta(days=7)

fecha_evento = st.date_input(
    "Selecciona la fecha del evento",
    value = hoy,        # valor por defecto: hoy
    min_value = hoy,    # fecha mínima: hoy
    max_value = limite  # fecha máxima: hoy + 7 días
)

st.write("Fecha seleccionada:", fecha_evento)

st.subheader("Selecciona un recurso")

if len(recursos) == 0:
    st.warning("No hay recursos registrados.")
else:
    recurso_items = {}
    for r in recursos:
        clave = f"{r['nombre']}"
        valor = r["id"]
        recurso_items[clave] = valor
    recurso_seleccionado = st.selectbox("Recurso:", list(recurso_items.keys()))
    recurso_id = recurso_items[recurso_seleccionado]

turno = st.selectbox("Selecciona el turno:", turnos)
if st.button("Reservar recurso"):
    try:
        reservar_recurso(cliente_id, recurso_id, fecha_evento.strftime("%Y-%m-%d"), turno)
        st.success(f"Recurso reservado para el cliente '{cliente_seleccionado}' el {fecha_evento} en el turno '{turno}'.")
    except Exception as e:
        st.error(f"Error al reservar el recurso: {str(e)}")


