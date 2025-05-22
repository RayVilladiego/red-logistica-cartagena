import streamlit as st
import pandas as pd

def mostrar_pedidos(df_pedidos):
    st.header("📝 Pedidos")
    st.dataframe(df_pedidos)

    # Aquí añade opciones para actualizar estado, agregar pedidos, etc.
