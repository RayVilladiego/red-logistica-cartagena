import streamlit as st
from database import get_orders

def show_orders():
    st.subheader("📦 Gestión de Pedidos")

    orders = get_orders()
    if not orders:
        st.warning("No hay pedidos registrados.")
        return

    st.dataframe(orders)

    st.markdown("---")
    if st.button("🔄 Actualizar pedidos"):
        st.experimental_rerun()
