import streamlit as st
from storage import cargar_datos, actualizar_estado
from storage_clientes import eliminar_cliente

actualizar_estado(cargar_datos())  # Asegurarnos de que el estado esté actualizado al cargar la página

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


st.title("Gestión de clientes")

# Estado para confirmar eliminación
if "cliente_a_eliminar" not in st.session_state:
    st.session_state["cliente_a_eliminar"] = None

datos = cargar_datos()
clientes = datos["gimnasio"]["clientes"]

# Filtrar solo activos
clientes_activos = []
for c in clientes:
    if c.get("estado", "ACTIVO") == "ACTIVO":
        clientes_activos.append(c)

if len(clientes_activos) == 0:
    st.info("No existen clientes activos actualmente.")
else:
    st.subheader("Selecciona un cliente")

    # Selectbox
    opciones = {}
    for c in clientes_activos:
        label = f"{c['nombre']} (ID {c['id']})"
        opciones[label] = c["id"]

    seleccion = st.selectbox("Selecciona un cliente:", list(opciones.keys()))
    cliente_id = opciones[seleccion]

    st.write(f"Cliente seleccionado: **{seleccion}**")

    # Buscar cliente seleccionado
    cliente_seleccionado = None
    for c in clientes_activos:
        if c["id"] == cliente_id:
            cliente_seleccionado = c
            break

    # Mostrar detalles del cliente
    st.write("### 📋 Detalles del cliente")
    st.write(f"**ID:** {cliente_seleccionado['id']}")
    st.write(f"**Nombre:** {cliente_seleccionado['nombre']}")
    st.write(f"**Edad:** {cliente_seleccionado.get('edad', 'No registrada')}")
    st.write(f"**Plan:** {cliente_seleccionado.get('plan', 'No asignado')}")

    if st.button("Eliminar cliente", type="primary"):
        st.session_state["cliente_a_eliminar"] = cliente_id

# Zona de confirmación
if st.session_state["cliente_a_eliminar"] is not None:
    st.warning(
        f"¿Seguro que deseas eliminar al cliente con ID {st.session_state['cliente_a_eliminar']}?",
        icon="⚠️"
    )

    col1, col2 = st.columns(2)

    if col1.button("Sí, eliminar"):

        try:
            msg = eliminar_cliente(st.session_state["cliente_a_eliminar"])
            st.success(msg)
            st.session_state["cliente_a_eliminar"] = None
            st.rerun()
        except Exception as e:
            st.error(str(e))

    if col2.button("No, cancelar"):
        st.session_state["cliente_a_eliminar"] = None
        st.info("Operación cancelada.")
