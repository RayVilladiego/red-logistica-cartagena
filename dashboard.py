import streamlit as st

def dashboard(data):
    st.title("Dashboard de Seguimiento")
    total = len(data)
    activos = sum(1 for d in data if d["estado"] == "Pendiente")
    en_ruta = sum(1 for d in data if d["estado"] == "En ruta")
    entregados = sum(1 for d in data if d["estado"] == "Entregado")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Pedidos", total)
    col2.metric("Pedidos Activos", activos)
    col3.metric("Pedidos En Ruta", en_ruta)
    col4.metric("Pedidos Entregados", entregados)
