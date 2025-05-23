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
    seleccion = st.sidebar.selectbox("Menu", menu)


    if not st.session_state["logueado"]:
        if st.sidebar.selectbox("Menu", menu) == "Login":
            login()
        else:
            home()
    else:
        choice = st.sidebar.radio("Ir a:", menu)
        if choice == "Inicio":
            home()
        elif choice == "Dashboard":
            # Aquí deberías obtener datos reales, por ejemplo:
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
