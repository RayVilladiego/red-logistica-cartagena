# dashboard.py

import streamlit as st
import pandas as pd
import datetime

def mostrar_dashboard():
    st.title("📊 Panel de KPIs Logísticos")
    st.subheader("Resumen general del sistema")

    # Simulación de KPIs (puedes conectar con base de datos real)
    pedidos_totales = 128
    pedidos_en_ruta = 37
    pedidos_entregados = 85
    porcentaje_entregado = (pedidos_entregados / pedidos_totales) * 100

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Pedidos en Ruta", pedidos_en_ruta)
    col2.metric("Pedidos Entregados", pedidos_entregados)
    col3.metric("Progreso", f"{porcentaje_entregado:.1f}%", delta="↑ 5.2%")

    st.divider()
    st.subheader("📍 Alertas por Congestión")

    zonas_congestionadas = ["Zona Norte", "Av Pedro Romero", "Centro Histórico"]
    st.warning("Alerta de tráfico detectada en: " + ", ".join(zonas_congestionadas))

    st.divider()
    st.subheader("🕒 Mejor horario sugerido para despachar")

    ahora = datetime.datetime.now()
    sugerencia = ahora.replace(hour=16, minute=0, second=0)
    st.info(f"Recomendación: Salir a las {sugerencia.strftime('%H:%M')} para evitar congestión.")

