import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import joblib
from tensorflow.keras.models import load_model
from datetime import datetime

# Configuración general
st.set_page_config(page_title="Red Logística Cartagena", layout="wide")

# Sidebar de navegación
with st.sidebar:
    st.title("📦 Red Logística Cartagena")
    st.write("Filtros y controles del sistema")
    estado_pedido = st.selectbox("📦 Estado del pedido", ["En camino", "Entregado", "Pendiente"])
    alerta_congestion = st.checkbox("⚠️ Mostrar zonas con congestión")
    hora_actual = st.slider("🕒 Hora de salida (24h)", 0, 23, 9)

# Modelo y scaler
model = load_model("modelo_entrega.h5")
scaler = joblib.load("scaler_entrega.pkl")
columnas_modelo = joblib.load("columnas_modelo.pkl")

# Simulación de ubicaciones
ubicaciones = {
    "Retail1": [10.39972, -75.51444],
    "Retail2": [10.4220, -75.5412],
    "Tienda3": [10.4238, -75.5253],
    "Almacén4": [10.3938, -75.4791],
    "Puerto5": [10.4242, -75.5505],
}

# Función para sugerir mejor franja horaria (simulada)
def sugerir_horario(distancia_km, clima, tipo_via):
    if clima == "Lluvioso" or tipo_via == "Terciaria":
        return "Evitar entre 6:00 a.m. y 8:00 a.m."
    elif distancia_km > 20:
        return "Recomendado entre 10:00 a.m. y 2:00 p.m."
    else:
        return "Sin restricciones críticas"

# Interfaz central
st.header("🧠 Estimador de Entrega Inteligente")
col1, col2 = st.columns(2)

with col1:
    origen = st.selectbox("🛫 Punto de origen", list(ubicaciones.keys()))
    destino = st.selectbox("📍 Punto de destino", list(ubicaciones.keys()), index=4)
    distancia_km = np.round(
        np.random.uniform(2, 25) if origen != destino else 0.5, 2
    )
    tipo_via = st.selectbox("🛣️ Tipo de vía", ["Primaria", "Secundaria", "Terciaria"])
    clima = st.selectbox("🌤️ Clima", ["Soleado", "Lluvioso", "Nublado"])

    # Codificación
    entrada = {
        "Distancia": distancia_km,
        "Tipo_via_Primaria": 1 if tipo_via == "Primaria" else 0,
        "Tipo_via_Secundaria": 1 if tipo_via == "Secundaria" else 0,
        "Clima_Lluvioso": 1 if clima == "Lluvioso" else 0,
        "Clima_Nublado": 1 if clima == "Nublado" else 0,
        "Hora": hora_actual
    }

    # Asegurar todas las columnas
    for col in columnas_modelo:
        if col not in entrada:
            entrada[col] = 0

    df_input = pd.DataFrame([entrada])
    df_scaled = scaler.transform(df_input)
    prediccion = model.predict(df_scaled)[0][0]
    st.success(f"⏱️ Tiempo estimado de entrega: {prediccion:.2f} minutos")
    st.info(f"🕒 Mejor horario para salir: {sugerir_horario(distancia_km, clima, tipo_via)}")

with col2:
    st.subheader("🗺️ Mapa interactivo de ruta")
    mapa = folium.Map(location=[10.41, -75.53], zoom_start=13)
    marcador = MarkerCluster().add_to(mapa)
    folium.Marker(location=ubicaciones[origen], tooltip="Origen", icon=folium.Icon(color="green")).add_to(marcador)
    folium.Marker(location=ubicaciones[destino], tooltip="Destino", icon=folium.Icon(color="red")).add_to(marcador)
    folium.PolyLine(locations=[ubicaciones[origen], ubicaciones[destino]],
                    color="blue", weight=3).add_to(mapa)

    if alerta_congestion:
        folium.Circle(
            location=ubicaciones["Retail2"],
            radius=300,
            color="orange",
            fill=True,
            tooltip="🚧 Congestión alta"
        ).add_to(mapa)

    st_data = st_folium(mapa, width=700, height=450)

# Pie de página
st.caption("🔍 Proyecto académico impulsado con redes neuronales - 2025")
