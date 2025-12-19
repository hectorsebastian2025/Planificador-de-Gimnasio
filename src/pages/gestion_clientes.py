import streamlit as st
from storage import cargar_datos, eliminar_cliente

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

    # Solo selectbox, sin buscador por ID
    opciones = {}
    for c in clientes_activos:
        label = f"{c['nombre']} (ID {c['id']})"
        opciones[label] = c["id"]

    seleccion = st.selectbox("Selecciona un cliente:", list(opciones.keys()))
    cliente_id = opciones[seleccion]

    st.write(f"Cliente seleccionado: **{seleccion}**")

    if st.button("Eliminar cliente", type="primary"):
        st.session_state["cliente_a_eliminar"] = cliente_id

# 🟡 Zona de confirmación
if st.session_state["cliente_a_eliminar"] is not None:
    st.warning(
        f"¿Seguro que deseas eliminar al cliente con ID {st.session_state['cliente_a_eliminar']}?",
        icon="⚠️"
    )

    col1, col2 = st.columns(2)

    if col1.button("Sí, eliminar"):
        from storage import eliminar_cliente
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
