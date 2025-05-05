import streamlit as st
import pandas as pd
from database import get_kpi_data

def show_dashboard():
    st.subheader("📊 KPIs de Entregas")
    datos = get_kpi_data()
    col1, col2, col3 = st.columns(3)
    col1.metric("✅ Entregados", datos['entregados'])
    col2.metric("🚚 En Ruta", datos['en_ruta'])
    col3.metric("📦 Pendientes", datos['pendientes'])
