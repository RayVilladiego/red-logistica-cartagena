def tracking_view(pedidos):
    import streamlit as st
    st.title("Tracking de Pedidos")
    pedido_id = st.number_input("ID Pedido", min_value=1)
    pedido = next((p for p in pedidos if p["id"] == pedido_id), None)
    if pedido:
        st.write(f"Pedido {pedido_id}: Estado {pedido['estado']} - Ruta {pedido['origen']} → {pedido['destino']}")
    else:
        st.error("Pedido no encontrado")
