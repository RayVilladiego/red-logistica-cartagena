import streamlit as st
import pandas as pd
from database import get_order_data

def show_orders():
    st.subheader("🧾 Gestión de Pedidos")
    df = get_order_data()
    st.dataframe(df)

    if st.button("📤 Exportar a Excel"):
        df.to_excel("pedidos_export.xlsx", index=False)
        st.success("Archivo exportado como 'pedidos_export.xlsx'")
