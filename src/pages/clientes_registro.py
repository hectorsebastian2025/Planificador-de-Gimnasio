import streamlit as st
from storage import cargar_objetos, guardar_datos, cargar_datos, agregar_cliente, actualizar_estado
from models import Cliente

datos = cargar_datos()
actualizar_estado(datos)
guardar_datos(datos)

# Ocultar completamente el sidebar original
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {display: none;}
</style>
""", unsafe_allow_html=True)


if st.sidebar.button("Menú Principal"):
    st.switch_page("./app_streamlit.py")
st.sidebar.write("Sección de clientes:")
with st.sidebar.expander("Clientes"):

    if st.button("Registro de clientes"):
        st.switch_page("pages/clientes_registro.py")

    if st.button("Gestión de clientes"):
        st.switch_page("pages/gestion_clientes.py")

st.sidebar.write("Sección de eventos:")

if st.sidebar.button("Gestión de eventos"):
    st.switch_page("pages/eventos.py")


# Vamos a cargar los datos
clientes = cargar_datos()["gimnasio"]["clientes"]

# Crear la interfaz para registrar al cliente
nombre = st.text_input("Nombre del cliente:")
edad = st.number_input("Edad del cliente:", min_value = 14, max_value = 120, step = 1)
planes = ["Básico", "Básico con entrenador", "Premium"]
plan = st.selectbox("Selecciona un plan:", planes)

if st.button("Registrar cliente"):
    try:
        nuevo_cliente = Cliente(
            id = len(clientes) + 1,
            nombre = nombre,
            edad = edad,
            plan = plan,
        )
        agregar_cliente(nuevo_cliente)
        st.success(f"Cliente '{nombre}' registrado exitosamente. Su número de identificación para el gimnasio es {nuevo_cliente.id}.")
    except Exception as e:
        st.error(f"Error al registrar el cliente: {str(e)}")