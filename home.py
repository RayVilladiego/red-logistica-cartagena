# home.py
import streamlit as st

def show_home():
    st.title("🏠 Bienvenido a la Red Logística Inteligente")
    st.markdown("""
    Esta plataforma permite el seguimiento en tiempo real de entregas, rutas inteligentes, visualización de KPI's y análisis predictivo mediante redes neuronales.
    
    ### Funcionalidades principales:
    - Visualización del **Dashboard logístico**
    - Seguimiento en tiempo real de pedidos
    - Predicción de rutas y tiempos estimados
    - Gestión de pedidos desde un solo lugar
    
    Selecciona una opción en el menú lateral para comenzar.
    """)
