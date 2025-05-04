import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np

# Título
st.set_page_config(page_title="Red Logística Cartagena", layout="wide")
st.title("📍 Red Logística - Seguimiento en tiempo real estilo Waze")

# KPIs simulados
col1, col2, col3 = st.columns(3)
col1.metric("Pedidos activos", "25", "+3 hoy")
col2.metric("Retrasos detectados", "4", "-1 vs ayer")
col3.metric("Entrega puntual (%)", "87%", "+5%")

# Coordenadas de ejemplo (Cartagena)
origen = [10.391049, -75.479426]  # Bocagrande
destino = [10.424903, -75.544122]  # Mamonal

# Crear mapa
m = folium.Map(location=origen, zoom_start=12)
folium.Marker(origen, tooltip="Origen: Bocagrande", icon=folium.Icon(color="blue")).add_to(m)
folium.Marker(destino, tooltip="Destino: Mamonal", icon=folium.Icon(color="green")).add_to(m)

# Simular ruta
folium.PolyLine([origen, destino], color="red", weight=3, opacity=0.8).add_to(m)

# Mostrar mapa
st.subheader("📌 Mapa de ruta logística")
st_data = st_folium(m, width=1200, height=600)
