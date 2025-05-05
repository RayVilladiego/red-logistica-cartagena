import streamlit as st
from login import login_section
from mapa import mapa_section
from dashboard import dashboard_section
from gestion_pedidos import pedidos_section

st.set_page_config(page_title="Red Logística Cartagena", layout="wide")

# Sesión de usuario
if "usuario" not in st.session_state:
    st.session_state["usuario"] = None

# Login
if st.session_state["usuario"] is None:
    login_section()
else:
    st.sidebar.title(f"Bienvenido, {st.session_state['usuario']}")
    seccion = st.sidebar.radio("Navegación", ["Mapa", "Dashboard", "Gestión de Pedidos"])

    if seccion == "Mapa":
        mapa_section()
    elif seccion == "Dashboard":
        dashboard_section()
    elif seccion == "Gestión de Pedidos":
        pedidos_section()

