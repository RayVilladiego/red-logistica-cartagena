import streamlit as st

# Importa tus vistas y funciones
from login import login
from dashboard import dashboard
from orders import orders_view
from tracking import tracking_view
from home import home
from predict import predict_view  # Asumiendo que tu función principal es predict_view()

def main():
    if "logueado" not in st.session_state:
        st.session_state["logueado"] = False

    # Menú general
    menu = ["Inicio", "Login", "Dashboard", "Órdenes", "Agregar Pedido", "Predicción", "Tracking", "Cerrar sesión"]

    seleccion = st.sidebar.radio("Ir a:", menu)

    # Lógica de navegación
    if not st.session_state["logueado"]:
        if seleccion == "Login":
            login()
        else:
            home()
    else:
        if seleccion == "Inicio":
            home()
        elif seleccion == "Dashboard":
            # Aquí deberías pasar los datos reales de pedidos desde tu base de datos
            # Ejemplo: pedidos = obtener_pedidos_de_tu_db()
            pedidos = []  # Sustituye con tu función real
            dashboard(pedidos)
        elif seleccion == "Órdenes":
            pedidos = []  # Sustituye con tu función real
            orders_view(pedidos)
        elif seleccion == "Agregar Pedido":
            # Aquí llamas la función que tienes en app.py para agregar pedidos
            # O puedes mover esa lógica a un módulo aparte si prefieres
            st.write("Aquí va tu formulario de agregar pedido (mueve el código desde app.py)")
        elif seleccion == "Predicción":
            predict_view()
        elif seleccion == "Tracking":
            pedidos = []  # Sustituye con tu función real
            tracking_view(pedidos)
        elif seleccion == "Cerrar sesión":
            st.session_state["logueado"] = False
            st.success("Sesión cerrada. Regresa a Login para ingresar.")

if __name__ == "__main__":
    main()

