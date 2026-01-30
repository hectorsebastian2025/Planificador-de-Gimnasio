import streamlit as st
from datetime import date, timedelta
from storage import cargar_objetos, guardar_datos, cargar_datos, reservar_recurso, actualizar_estado, alternativa_reservar_recurso

datos = cargar_datos()
actualizar_estado(datos)
guardar_datos(datos)

clientes = datos["gimnasio"]["clientes"]
recursos = datos["gimnasio"]["recursos"]
turnos = datos["gimnasio"]["horario"]["turnos"]

# Ocultar completamente el sidebar original
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {display: none;}
</style>
""", unsafe_allow_html=True)



# --- 6. Sidebar personalizado ---
if st.sidebar.button("Menú Principal"):
    st.switch_page("app_streamlit.py")


st.sidebar.markdown("---")

with st.sidebar:
    st.markdown("### Sección de Clientes")
    if st.button("📝 Registro de Clientes", key="sidebar_registro"):
        st.switch_page("pages/clientes_registro.py")
    if st.button("📋 Gestión de Clientes", key="sidebar_gestion"):
        st.switch_page("pages/gestion_clientes.py")



with st.sidebar:
    st.markdown("### Sección de Eventos")
    if st.button("📅 Reservación de Evento", key="sidebar_reservar"):
        st.switch_page("pages/eventos.py")
    if st.button("🎯 Gestión de Eventos", key="sidebar_eventos"):
        st.switch_page("pages/gestion_eventos.py")

st.sidebar.markdown("---")



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
        reservar_recurso(
            cliente_id,
            recurso_id,
            fecha_evento.strftime("%Y-%m-%d"),
            turno
        )
        st.success(
            f"Recurso reservado para el cliente '{cliente_seleccionado}' "
            f"el {fecha_evento} en el turno '{turno}'."
        )

    except Exception as e:
        st.error(f"Error al reservar el recurso: {str(e)}")

        alternativas = alternativa_reservar_recurso(
            cliente_id,
            recurso_id,
            fecha_evento.strftime("%Y-%m-%d"),
            turno
        )

        if len(alternativas) == 0:
            st.info("No hay alternativas disponibles.")
        else:
            st.subheader("Alternativas sugeridas:")
            for alt in alternativas:
                st.write(f"📅 {alt[0]} ⏰ {alt[1]}")
