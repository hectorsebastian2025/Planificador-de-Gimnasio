import streamlit as st
from storage import cargar_datos, guardar_datos, actualizar_estado


actualizar_estado(cargar_datos())  # Asegurarnos de que el estado esté actualizado al cargar la página

# --- Cargar datos ---
datos = cargar_datos()
clientes = datos["gimnasio"]["clientes"]
reservas = datos["gimnasio"].get("reservas", [])

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


st.title("Gestión de Reservas - Cancelar Evento")

# --- Selección de cliente ---
opciones_clientes = {}
for c in clientes:
    if c["estado"] == "INACTIVO":
        continue
    opciones_clientes[f"{c['nombre']} (ID {c['id']})"] = c["id"]

cliente_seleccionado = st.selectbox("Selecciona un cliente:", list(opciones_clientes.keys()))
cliente_id = opciones_clientes[cliente_seleccionado]

# --- Mostrar reservas activas ---
st.subheader(f"Reservas activas de {cliente_seleccionado}")
reservas_activas = []
for r in reservas:
    if r["cliente_id"] == cliente_id and r["estado"] == "ACTIVA":
        reservas_activas.append(r)

if len(reservas_activas) == 0:
    st.info("No hay reservas activas para este cliente.")
else:
    for r in reservas_activas:
        # Obtener nombre del recurso
        recurso_nombre = ""
        for rec in datos["gimnasio"]["recursos"]:
            if rec["id"] == r["recurso_id"]:
                recurso_nombre = rec["nombre"]
                break
        
        # Creamos un contenedor para agrupar cada evento
        with st.container():
            col1, col2 = st.columns([3, 1])
            col1.write(f"{recurso_nombre} | {r['fecha']} | {r['turno']}")

            # Botón para iniciar confirmación
            if col2.button("Cancelar", key=f"cancelar_{r['id']}"):
                st.session_state[f"confirmar_{r['id']}"] = True

            # Mostrar confirmación justo debajo del evento
            if st.session_state.get(f"confirmar_{r['id']}", False):
                st.warning("¿Seguro que quieres cancelar esta reserva?")
                c_yes, c_no = st.columns(2)
                if c_yes.button("Sí", key=f"si_{r['id']}"):
                    for res in reservas:
                        if res["id"] == r["id"]:
                            res["estado"] = "CANCELADA"
                            guardar_datos(datos)
                            st.success(f"Reserva ID {res['id']} cancelada correctamente.")
                            break
                    del st.session_state[f"confirmar_{r['id']}"]
                if c_no.button("No", key=f"no_{r['id']}"):
                    st.info("Cancelación abortada.")
                    del st.session_state[f"confirmar_{r['id']}"]
