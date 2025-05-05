# app.py

import streamlit as st
from auth import show_login
from dashboard import show_dashboard
from tracking import show_tracking
from orders import show_orders
from routes import show_route
from home import show_home

# Diccionario de páginas con emojis para visualización
PAGINAS = {
    "🏠 Inicio": show_home,
    "📊 Dashboard": show_dashboard,
    "📍 Seguimiento": show_tracking,
    "🧾 Pedidos": show_orders,
    "🧠 Ruta Inteligente": show_route
}

def main():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        show_login()
    else:
        st.sidebar.title("📋 Menú de Navegación")
        seleccion = st.sidebar.radio("Ir a:", list(PAGINAS.keys()))
        PAGINAS[seleccion]()  # Ejecuta la función correspondiente

if __name__ == "__main__":
    main()
