import streamlit as st
import os
from PIL import Image
from storage import cargar_datos, actualizar_estado, guardar_datos

datos = cargar_datos()
actualizar_estado(datos)
guardar_datos(datos)

# --- 1. Obtener ruta del logo ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "..", "assets", "logo.png")
LOGO_PATH = os.path.normpath(LOGO_PATH)

# --- 2. Abrir y redimensionar la imagen ---
imagen = Image.open(LOGO_PATH)

# Ajusta el tamaño manteniendo proporción
ancho_deseado = 300
alto_proporcional = int(imagen.height * (ancho_deseado / imagen.width))
imagen = imagen.resize((ancho_deseado, alto_proporcional))

# --- 3. Mostrar en Streamlit centrado ---
col1, col2, col3 = st.columns([1,2,1])  # centrar el logo
with col2:
    st.image(
        imagen,
        use_container_width=False  # respeta el tamaño que pusimos
    )

st.markdown("<h3 style='text-align: center; margin-left: -64px; margin-top: -50px'; margin-right: -64px;'>Bienvenido al panel principal del planificador del gimnasio 💻</h3>", unsafe_allow_html=True)

# Ocultar el sidebar original
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {display: none;}
</style>
""", unsafe_allow_html=True)


# Navegación entre páginas

st.write("Sección de clientes:")

col1, col2 = st.columns(2)
with col1:
    if st.button("Registrar cliente"):
        st.switch_page("pages/clientes_registro.py")
with col2:
    if st.button("Gestión de clientes"):
        st.switch_page("pages/gestion_clientes.py")


# --- 6. Sidebar personalizado ---
st.sidebar.markdown("<h2 style='text-align: center; '> Menú Principal</h2>", unsafe_allow_html=True)


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

st.write("Sección de eventos:")
col1, col2 = st.columns(2)
with col1:
    if st.button("Reservar evento"):
        st.switch_page("pages/eventos.py")
    
with col2:
    if st.button("Gestión de Eventos"):
        st.switch_page("pages/gestion_eventos.py")

