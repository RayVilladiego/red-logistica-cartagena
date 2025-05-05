# dashboard.py

import streamlit as st
import pandas as pd
import numpy as np

def show_dashboard():
    st.title("📊 Dashboard Logístico")

    # Simulación de datos
    pedidos_entregados = 124
    pedidos_pendientes = 36
    promedio_tiempo = 42  # minutos
    porcentaje_retrasos = 18  # %

    st.metric("📦 Pedidos Entregados", pedidos_entregados)
    st.metric("⏳ Pedidos Pendientes", pedidos_pendientes)
    st.metric("🚚 Tiempo Promedio Entrega", f"{promedio_tiempo} min")
    st.metric("⚠️ % Retrasos", f"{porcentaje_retrasos}%")

    st.markdown("---")
    st.subheader("Histórico de entregas por día")
    fechas = pd.date_range(end=pd.Timestamp.today(), periods=7)
    entregas = np.random.randint(10, 30, size=7)
    df = pd.DataFrame({"Fecha": fechas, "Entregas": entregas})
    st.line_chart(df.set_index("Fecha"))

    st.markdown("---")
    st.subheader("Distribución de pedidos por zona")
    zonas = ["Norte", "Sur", "Centro", "Oriente", "Occidente"]
    valores = np.random.randint(10, 50, size=5)
    st.bar_chart(pd.DataFrame({"Zonas": zonas, "Pedidos": valores}).set_index("Zonas"))
