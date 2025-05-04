import streamlit as st
import pandas as pd
import joblib
import folium
from streamlit_folium import st_folium
from tensorflow.keras.models import load_model
import datetime
import openrouteservice
from openrouteservice import convert
import plotly.graph_objects as go

# Configuración general
st.set_page_config(layout="wide")
st.title("📦 Red Logística Inteligente - Cartagena")

# Parámetros iniciales
cliente = st.sidebar.selectbox("🧑‍💼 Cliente", ["Alfa S.A.S", "Beta Express", "Logística Total"])
estado_pedido = st.sidebar.selectbox("📦 Estado del pedido", ["En preparación", "En ruta", "Entregado"])
alerta = st.sidebar.selectbox("🚨 Alerta", ["Sin alertas", "Demora > 15 min", "Retraso crítico"])

# Horario de salida
hora_actual = st.slider("🕒 Hora de salida (24h)", 0, 23, 9)

# Modelo y scaler
model = load_model("modelo_entrega.h5", compile=False)
scaler = joblib.load("scaler_entrega.pkl")
columnas_modelo = joblib.load("columnas_modelo.pkl")

# Mapa editable
st.subheader("🗺️ Selecciona origen y destino en el mapa")

lat_inicial = 10.4
lon_inicial = -75.5
m = folium.Map(location=[lat_inicial, lon_inicial], zoom_start=12)

origen = folium.Marker(location=[10.4, -75.5], draggable=True, popup="📍 Origen").add_to(m)
destino = folium.Marker(location=[10.42, -75.55], draggable=True, popup="🏁 Destino").add_to(m)

map_data = st_folium(m, width=700, height=500)

# Obtener coordenadas editadas
coordenadas = map_data.get("last_object_clicked")

if coordenadas:
    latitud = coordenadas["lat"]
    longitud = coordenadas["lng"]
else:
    latitud = 10.4
    longitud = -75.5

# Simular variables para el modelo
entrada = {
    "Distancia": 5.2,
    "Hora": hora_actual,
    "Clima_Lluvioso": 0,
    "Clima_Soleado": 1,
    "Clima_Nublado": 0,
    "Tipo_via_Primaria": 1,
    "Tipo_via_Secundaria": 0,
    "Tipo_via_Terciaria": 0
}
for col in columnas_modelo:
    if col not in entrada:
        entrada[col] = 0

df_input = pd.DataFrame([entrada])
df_scaled = scaler.transform(df_input)
prediccion = model.predict(df_scaled)[0][0]

# KPI y sugerencia
def sugerir_horario(distancia_km):
    if distancia_km > 10:
        return "📌 6:00 a.m. (menos tráfico)"
    elif distancia_km > 5:
        return "📌 7:00 a.m."
    else:
        return "📌 8:00 a.m."

st.success(f"⏱️ Tiempo estimado de entrega: {prediccion:.2f} minutos")
st.info(f"🕒 Mejor horario para salir: {sugerir_horario(entrada['Distancia'])}")

# KPI logísticos
st.subheader("📊 KPIs del pedido")
col1, col2, col3 = st.columns(3)
col1.metric("Estado", estado_pedido)
col2.metric("Alerta", alerta)
col3.metric("Porcentaje entregado", "85%")

# Exportar resultados
st.download_button("📁 Exportar predicción", data=df_input.to_csv(index=False), file_name="prediccion_entrega.csv")

# Ruta simulada con OpenRouteService
st.subheader("🚚 Ruta óptima (simulada)")
try:
    client = openrouteservice.Client(key="TU_API_KEY_AQUI")  # Sustituye por tu API Key válida
    coords = ((-75.5, 10.4), (-75.55, 10.42))
    routes = client.directions(coords)
    geometry = routes["routes"][0]["geometry"]
    decoded = convert.decode_polyline(geometry)

    m_ruta = folium.Map(location=[10.41, -75.52], zoom_start=13)
    folium.PolyLine(locations=[(coord[1], coord[0]) for coord in decoded["coordinates"]],
                    color="blue", weight=5).add_to(m_ruta)
    st_folium(m_ruta, width=700, height=500)
except Exception as e:
    st.warning("No se pudo cargar la ruta simulada. Verifica tu API Key.")

