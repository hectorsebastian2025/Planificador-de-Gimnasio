import streamlit as st
from storage import cargar_objetos, guardar_datos, cargar_datos, agregar_cliente, contar_clientes
from models import Cliente

st.subheader("Cantidad de Clientes actuales")
st.info(f"Número de clientes registrados: {contar_clientes()}")
