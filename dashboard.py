import streamlit as st

def show_dashboard():
    st.title("Dashboard de Avance")
    st.metric("Horas estimadas", 1000)
    st.metric("Horas reales", 650)
    st.metric("Porcentaje completado", "65%")
