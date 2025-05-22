import streamlit as st
from login import login
from dashboard import dashboard
from orders import orders_view
from tracking import tracking_view
from home import home

def main():
    if "logueado" not in st.session_state:
        st.session_state["logueado"] = False

    menu = ["Inicio", "Login", "Dashboard", "Órdenes", "Tracking", "Cerrar sesión"]

    if not st.session_state["logueado"]:
        choice = st.sidebar.selectbox("Menú", ["Inicio", "Login"])
        if choice == "Login":
            login()
        else:
            home()
    else:
        choice = st.sidebar.selectbox("Menú", menu)
        if choice == "Inicio":
            home()
        elif choice == "Dashboard":
            # Aquí podrías obtener datos reales o simulados
            pedidos = [
                {"id": 1, "origen": "Cartagena", "destino": "Barranquilla", "estado": "En ruta"},
                {"id": 2, "origen": "Cartagena", "destino": "Santa Marta", "estado": "Pendiente"},
            ]
            dashboard(pedidos)
        elif choice == "Órdenes":
            pedidos = [
                {"id": 1, "origen": "Cartagena", "destino": "Barranquilla", "estado": "En ruta"},
                {"id": 2, "origen": "Cartagena", "destino": "Santa Marta", "estado": "Pendiente"},
            ]
            orders_view(pedidos)
        elif choice == "Tracking":
            pedidos = [
                {"id": 1, "origen": "Cartagena", "destino": "Barranquilla", "estado": "En ruta"},
                {"id": 2, "origen": "Cartagena", "destino": "Santa Marta", "estado": "Pendiente"},
            ]
            tracking_view(pedidos)
        elif choice == "Cerrar sesión":
            st.session_state["logueado"] = False
            st.success("Sesión cerrada")

if __name__ == "__main__":
    main()
