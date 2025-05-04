import streamlit as st
import pandas as pd
import numpy as np
import joblib
import pydeck as pdk
import datetime
from tensorflow.keras.models import load_model

# Cargar modelo y scaler
model = load_model("modelo_entrega.h5")
scaler = joblib.load("scaler_entrega.pkl")
columnas_modelo = joblib.load("columnas_modelo.pkl")

# Sidebar
st.sidebar.title("📦 Filtro de Pedidos")
filtro_estado = st.sidebar.selectbox("Estado del Pedido", ["Todos", "Pendiente", "En camino", "Entregado"])
filtro_alerta = st.sidebar.selectbox("Alerta de Tramo", ["Todas", "Alta congestión", "Tramo libre"])

# Título
st.title("🚚 Red Logística Inteligente en Cartagena")
st.markdown("Predice el **tiempo estimado de entrega** y visualiza el estado del tráfico en tiempo real.")

# Inputs
origen = st.selectbox("📍 Origen", ["Centro de Distribución", "Puerto1", "Puerto2"])
destino = st.selectbox("🏪 Destino", ["Retail1", "Retail2", "Tienda3", "Almacén4", "Puerto5"])

distancia = st.slider("📏 Distancia (km)", 2.0, 30.0, step=0.5)

tipo_via = st.selectbox("🛣️ Tipo de vía", ["Principal", "Secundaria", "Terciaria"])
clima = st.selectbox("⛅ Clima", ["Soleado", "Lluvia", "Tormenta"])

hora_actual = st.time_input("🕐 Hora de salida", datetime.time(8, 0))
franja_horaria = (
    "Mañana" if 6 <= hora_actual.hour < 12
    else "Tarde" if 12 <= hora_actual.hour < 18
    else "Noche"
)

# Preparar entrada
input_dict = {
    "distancia": distancia,
    "tipo_via_Principal": 1 if tipo_via == "Principal" else 0,
    "tipo_via_Secundaria": 1 if tipo_via == "Secundaria" else 0,
    "tipo_via_Terciaria": 1 if tipo_via == "Terciaria" else 0,
    "clima_Lluvia": 1 if clima == "Lluvia" else 0,
    "clima_Soleado": 1 if clima == "Soleado" else 0,
    "clima_Tormenta": 1 if clima == "Tormenta" else 0,
    "hora_Mañana": 1 if franja_horaria == "Mañana" else 0,
    "hora_Tarde": 1 if franja_horaria == "Tarde" else 0,
    "hora_Noche": 1 if franja_horaria == "Noche" else 0,
}
for col in columnas_modelo:
    if col not in input_dict:
        input_dict[col] = 0

input_df = pd.DataFrame([input_dict])
input_scaled = scaler.transform(input_df)

# Predicción
if st.button("📊 Estimar tiempo de entrega"):
    prediccion = model.predict(input_scaled)
    tiempo_estimado = round(prediccion[0][0], 2)
    st.success(f"🕒 Tiempo estimado de entrega: {tiempo_estimado} minutos")

# Mapa interactivo
st.subheader("🗺️ Visualización de ruta en Cartagena (simulada)")
map_data = pd.DataFrame({
    'lat': [10.400, 10.405],
    'lon': [-75.500, -75.495],
    'label': ['Origen', 'Destino']
})

layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_data,
    get_position='[lon, lat]',
    get_color='[255, 140, 0, 160]',
    get_radius=120,
)

st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/dark-v10",
    initial_view_state=pdk.ViewState(latitude=10.402, longitude=-75.497, zoom=13),
    layers=[layer],
    tooltip={"text": "{label}"}
))

st.markdown("---")
st.markdown("📘 Proyecto académico desarrollado por **Will Andrés Herazo** y **Raylin Villadiego**.")
