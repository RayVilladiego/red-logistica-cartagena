import streamlit as st
import folium
from streamlit_folium import st_folium

def show_tracking():
    st.subheader("📍 Seguimiento de Entregas en Tiempo Real")

    m = folium.Map(location=[10.391, -75.479], zoom_start=13)
    
    folium.Marker(location=[10.391, -75.479], popup="Origen", icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(location=[10.410, -75.505], popup="Destino", icon=folium.Icon(color="red")).add_to(m)
    folium.PolyLine(locations=[[10.391, -75.479], [10.410, -75.505]], color="blue").add_to(m)

    st_folium(m, width=700, height=500)

    st.markdown("🔄 Actualizado en tiempo real. Esta visualización muestra el estado actual de la entrega en curso.")
