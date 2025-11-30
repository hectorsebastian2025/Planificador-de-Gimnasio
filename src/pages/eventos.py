import streamlit as st
from datetime import date, timedelta

hoy = date.today()
limite = hoy + timedelta(days=30)

fecha_evento = st.date_input(
    "Selecciona la fecha del evento",
    value = hoy,        # valor por defecto: hoy
    min_value = hoy,    # fecha mínima: hoy
    max_value = limite  # fecha máxima: hoy + 30 días
)

st.write("Fecha seleccionada:", fecha_evento)