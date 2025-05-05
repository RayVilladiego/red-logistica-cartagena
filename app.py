# app.py
import streamlit as st
from auth import login
from dashboard import show_dashboard
from tracking import show_tracking
from orders import show_orders
from home import show_home
from routes import show_routes
from database import init_db

# Inicializar la base de datos
init_db()

# Login
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    login()
else:
    st.sidebar.title("Navegación")
    page = st.sidebar.radio("Ir a", ["Inicio", "Dashboard", "Seguimiento", "Pedidos", "Rutas"])

    if page == "Inicio":
        show_home()
    elif page == "Dashboard":
        show_dashboard()
    elif page == "Seguimiento":
        show_tracking()
    elif page == "Pedidos":
        show_orders()
    elif page == "Rutas":
        show_routes()


