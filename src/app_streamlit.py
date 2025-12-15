import streamlit as st
from storage import cargar_datos, actualizar_estado, guardar_datos

datos = cargar_datos()
actualizar_estado(datos)
guardar_datos(datos)

st.set_page_config(page_title="Gestor del Gimnasio", page_icon="💪", layout="centered")

st.title("🏋️‍♂️ Sistema de Gestión del Gimnasio")
st.write("Bienvenido al panel principal del planificador del gimnasio.")

# Ocultar completamente el sidebar original
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {display: none;}
</style>
""", unsafe_allow_html=True)


# Navegación entre páginas

st.write("Navega a las diferentes secciones usando los botones a continuación:")
st.write("Sección de clientes:")

col1, col2 = st.columns(2)
with col1:
    if st.button("Registrar cliente"):
        st.switch_page("pages/clientes_registro.py")
with col2:
    if st.button("Gestión de clientes"):
        st.switch_page("pages/gestion_clientes.py")


st.sidebar.title("Menú principal")

with st.sidebar.expander("Clientes"):
    if st.button("Registro de clientes"):
        st.switch_page("pages/clientes_registro.py")

    if st.button("Gestión de clientes"):
        st.switch_page("pages/gestion_clientes.py")

st.write("Sección de eventos:")

col1, col2 = st.columns(2)
with col1:
    if st.button("Reservar evento"):
        st.switch_page("pages/eventos.py")
    
with col2:
    if st.button("Gestión de Eventos"):
        st.switch_page("pages/gestion_eventos.py")

