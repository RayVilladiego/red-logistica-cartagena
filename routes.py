import streamlit as st
from login import login
from dashboard import dashboard
from orders import orders_view
from tracking import tracking_view
from home import home
from database import get_orders
from predict import predict_view

def main():
    if "logueado" not in st.session_state:
        st.session_state["logueado"] = False

    menu = ["Inicio", "Login", "Dashboard", "Órdenes", "Tracking", "Predicción", "Cerrar sesión"]

    if not st.session_state["logueado"]:
        seleccion = st.sidebar.selectbox("Menu", menu)
        if seleccion == "Login":
            login()
        else:
            home()
    else:
        seleccion = st.sidebar.selectbox("Menu", menu)
        if seleccion == "Inicio":
            home()
        elif seleccion == "Dashboard":
            pedidos_df = get_orders()
            pedidos = pedidos_df.to_dict(orient="records")
            dashboard(pedidos)
        elif seleccion == "Órdenes":
            pedidos_df = get_orders()
            pedidos = pedidos_df.to_dict(orient="records")
            orders_view(pedidos)
        elif seleccion == "Tracking":
            pedidos_df = get_orders()
            pedidos = pedidos_df.to_dict(orient="records")
            tracking_view(pedidos)
        elif seleccion == "Predicción":
            predict_view()
        elif seleccion == "Cerrar sesión":
            st.session_state["logueado"] = False
            st.success("Sesión cerrada")

if __name__ == "__main__":
    main()
