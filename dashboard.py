import streamlit as st
import pandas as pd

def mostrar_dashboard(df_pedidos):
    st.header("📈 Dashboard de Seguimiento")

    pedidos_activos = df_pedidos[df_pedidos['estado'] == 'activo'].shape[0]
    pedidos_entregados = df_pedidos[df_pedidos['estado'] == 'entregado'].shape[0]
    pedidos_en_ruta = df_pedidos[df_pedidos['estado'] == 'en ruta'].shape[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("🚚 Pedidos Activos", pedidos_activos)
    col2.metric("✅ Pedidos Entregados", pedidos_entregados)
    col3.metric("🛣️ Pedidos en Ruta", pedidos_en_ruta)

    # Aquí puedes agregar gráficos, tablas o mapas para seguimiento visual

# Ejemplo de uso:
# df_pedidos = pd.read_csv('pedidos.csv')  # o desde base datos
# mostrar_dashboard(df_pedidos)
