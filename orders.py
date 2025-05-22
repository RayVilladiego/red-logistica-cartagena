def orders_view(pedidos):
    import streamlit as st
    st.title("Gestión de Órdenes")
    for pedido in pedidos:
        st.write(f"ID: {pedido['id']} - {pedido['origen']} → {pedido['destino']} - Estado: {pedido['estado']}")
