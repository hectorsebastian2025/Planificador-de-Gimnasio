import streamlit as st
from storage import cargar_objetos, guardar_datos, cargar_datos
from models import Cliente

# Vamos a cargar los datos
clientes = cargar_datos()["gimnasio"]["clientes"]

# Crear la interfaz para registrar al cliente
nombre = st.text_input("Nombre del cliente:")
edad = st.number_input("Edad del cliente:", min_value = 14, max_value = 120, step = 1)
planes = ["Básico", "Básico con etrenador", "Premium"]
plan = st.selectbox("Selecciona un plan:", planes)

