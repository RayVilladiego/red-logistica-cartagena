import streamlit as st
import numpy as np
import pandas as pd
import joblib
from tensorflow.keras.models import load_model

# ------------------------ Configuración de la página ------------------------
st.set_page_config(
    page_title="Estimador Logístico Cartagena",
    page_icon="🚚",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ------------------------ Barra lateral con info ------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063822.png", width=100)
    st.title("📦 Red Logística")
    st.markdown("""
    Esta aplicación predice el **tiempo estimado de entrega** de productos en Cartagena,
    considerando distancia, tipo de vía y clima.  
    Desarrollado por **Will Andrés Herazo** para una red logística inteligente en la ciudad.
    """)
    st.markdown("📍 Proyecto académico con redes neuronales y aprendizaje automático.")

# ------------------------ Cargar modelos ------------------------
model = load_model("modelo_entrega.h5")
scaler = joblib.load("scaler_entrega.pkl")

# ------------------------ Encabezado principal ------------------------
st.markdown("<h1 style='text-align: center;'>🚛 Estimador de Entregas Cartagena</h1>", unsafe_allow_html=True)
st.markdown("#### 🗺️ Completa los datos logísticos:")

# ------------------------ Inputs del usuario ------------------------
origen = st.selectbox("📍 Punto de origen:", ["Retail1", "Retail2", "Tienda3", "Almacén4"])
destino = st.selectbox("🏁 Punto de destino:", ["Puerto5", "Puerto6", "Tienda7", "Bodega8"])
distancia = st.slider("📏 Distancia (km):", min_value=2.0, max_value=30.0, step=0.5)

tipo_via = st.selectbox("🛣️ Tipo de vía:", ["Principal", "Secundaria", "Terciaria"])
clima = st.selectbox("🌤️ Condiciones climáticas:", ["Soleado", "Lluvioso", "Nublado"])

# ------------------------ Codificar variables ------------------------
tipo_via_map = {"Principal": 0, "Secundaria": 1, "Terciaria": 2}
clima_map = {"Soleado": 0, "Lluvioso": 1, "Nublado": 2}

# Features de entrada
input_data = pd.DataFrame({
    "Distancia": [distancia],
    "Tipo_via": [tipo_via_map[tipo_via]],
    "Clima": [clima_map[clima]]
})

input_scaled = scaler.transform(input_data)

# ------------------------ Predicción ------------------------
prediccion = model.predict(input_scaled)
tiempo_estimado = round(prediccion[0][0], 2)

# ------------------------ Resultado ------------------------
st.markdown("### ⏱️ Resultado de la predicción:")
st.success(f"🕐 Tiempo estimado de entrega: **{tiempo_estimado} minutos**")

# ------------------------ Pie de página ------------------------
st.markdown("---")
st.markdown("<center>💡 Proyecto académico - 2025</center>", unsafe_allow_html=True)

