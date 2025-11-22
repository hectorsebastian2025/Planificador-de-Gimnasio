import streamlit as st

st.set_page_config(page_title="Gestor del Gimnasio", page_icon="💪", layout="centered")

st.title("🏋️‍♂️ Sistema de Gestión del Gimnasio")
st.write("Bienvenido al panel principal del planificador del gimnasio.")

st.subheader("Secciones disponibles:")

col1, col2 = st.columns(2)

with col1:
    if st.button("Eventos"):
        st.switch_page("pages/eventos.py")

with col2:
    if st.button("Clientes"):
        st.switch_page("pages/clientes.py")