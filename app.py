
import streamlit as st
import pandas as pd
import joblib
import folium
folium.Marker(location=[lat, lon], draggable=True, popup="Mover este punto").add_to(m)
from streamlit_folium import st_folium
from tensorflow.keras.models import load_model
import datetime

# Configuración de la página
st.set_page_config(page_title="Red Logística Inteligente", layout="wide")
st.title("🚚 Red Logística Inteligente")

# Cargar modelo, scaler y columnas
model = load_model("modelo_entrega.h5", compile=False)
scaler = joblib.load("scaler_entrega.pkl")
columnas_modelo = joblib.load("columnas_modelo.pkl")

# Sidebar para filtros
with st.sidebar:
    st.header("📦 Filtros de pedidos")
    estado = st.selectbox("Estado del pedido", ["En ruta", "Entregado", "Pendiente"])
    alerta = st.selectbox("Zona en alerta", ["Ninguna", "Zona Norte", "Zona Industrial", "Centro Histórico"])

# Mapa editable
st.subheader("🗺️ Selecciona los puntos de origen y destino")

m = folium.Map(location=[10.4, -75.5], zoom_start=12)
origen = folium.Marker(location=[10.4, -75.5], draggable=True, popup="Origen", icon=folium.Icon(color="green"))
destino = folium.Marker(location=[10.43, -75.52], draggable=True, popup="Destino", icon=folium.Icon(color="red"))
origen.add_to(m)
destino.add_to(m)

map_data = st_folium(m, width=700, height=450)
st.write("🔄 Arrastra los puntos en el mapa para ajustar tu ruta.")

# Simulación de entrada de datos
st.subheader("🧠 Parámetros de la entrega")
distancia_km = st.slider("Distancia estimada (km)", 1.0, 30.0, 10.0)
tipo_via = st.selectbox("Tipo de vía", ["Primaria", "Secundaria"])
clima = st.selectbox("Condición climática", ["Soleado", "Lluvioso", "Nublado"])
hora_actual = datetime.datetime.now().hour

# Procesamiento de entrada
entrada = {
    "Distancia": distancia_km,
    "Hora": hora_actual,
    "Tipo_via_Primaria": 1 if tipo_via == "Primaria" else 0,
    "Tipo_via_Secundaria": 1 if tipo_via == "Secundaria" else 0,
    "Clima_Lluvioso": 1 if clima == "Lluvioso" else 0,
    "Clima_Nublado": 1 if clima == "Nublado" else 0,
    "Clima_Soleado": 1 if clima == "Soleado" else 0,
}

# Asegurar que todas las columnas estén presentes
for col in columnas_modelo:
    if col not in entrada:
        entrada[col] = 0

df_input = pd.DataFrame([entrada])
df_scaled = scaler.transform(df_input)

# Predicción
prediccion = model.predict(df_scaled)[0][0]
st.success(f"⏱️ Tiempo estimado de entrega: {prediccion:.2f} minutos")

# Recomendación de horario
def sugerir_horario(distancia):
    if distancia <= 5:
        return "8:00 - 10:00"
    elif distancia <= 15:
        return "6:00 - 8:00"
    else:
        return "5:00 - 7:00"

st.info(f"🕒 Mejor horario para salir: {sugerir_horario(distancia_km)}")

# KPIs logísticos
st.subheader("📊 Indicadores clave")
col1, col2, col3 = st.columns(3)
col1.metric("Estado actual", estado)
col2.metric("Zona crítica", alerta)
col3.metric("📦 Pedido entregado (%)", f"{round((1 if estado=='Entregado' else 0.5)*100)}%")

# Exportación a Excel
df_resultado = pd.DataFrame({
    "Distancia (km)": [distancia_km],
    "Clima": [clima],
    "Tipo de vía": [tipo_via],
    "Hora": [hora_actual],
    "Tiempo estimado (min)": [prediccion]
})

st.download_button("📥 Exportar resultados a Excel", data=df_resultado.to_csv(index=False).encode('utf-8'), file_name="resultado_entrega.csv", mime="text/csv")
