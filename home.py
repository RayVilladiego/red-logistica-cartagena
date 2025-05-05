import streamlit as st

def show_home():
    st.title("📦 Sistema de Reparto Inteligente")
    st.markdown("""
        Bienvenido al sistema logístico de Cartagena. Desde aquí puedes navegar por las funciones clave:
        - Seguimiento de pedidos
        - Predicción de entrega por red neuronal
        - Rutas recomendadas según condiciones
        - Dashboard con KPIs y exportación de datos
    """)
