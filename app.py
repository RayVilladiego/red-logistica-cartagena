import streamlit as st
import numpy as np
import pandas as pd
import joblib
from tensorflow.keras.models import load_model

# Cargar modelo y scaler
model = load_model("modelo_entrega.h5", compile=False)
scaler = joblib.load("scaler_entrega.pkl")

# -------- INTERFAZ --------
st.set_page_config(
    page_title="Red Logística Cartagena",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.markdown("🚚 **Red Logística**", unsafe_allow_html=True)
    st.markdown(
        """
        Esta aplicación predice el **tiempo estimado de entrega** de productos en Cartagena, 
        considerando distancia, tipo de vía y clima.

        **Desarrollado por Raylin Villadiego** para una red logística inteligente en la ciudad.

        🎯 Proyecto académico con redes neuronales y aprendizaje automático.
        """
    )

st.title("📦 Estimador Logístico Cartagena")

# Entrada de datos
origen = st.selectbox("Seleccione el punto de origen:", ["Retail1", "Retail2", "Tienda3", "Almacén4", "Puerto5"])
distancia = st.slider("Distancia (km)", 2, 30, 10)
tipo_via = st.selectbox("Tipo de vía", ["Principal", "Secundaria"])
clima = st.selectbox("Clima", ["Soleado", "Lluvioso", "Nublado"])

# Codificación manual
map_via = {"Principal": 0, "Secundaria": 1}
map_clima = {"Soleado": 0, "Lluvioso": 1, "Nublado": 2}
map_origen = {"Retail1": 0, "Retail2": 1, "Tienda3": 2, "Almacén4": 3, "Puerto5": 4}

# Crear array de entrada
input_data = np.array([[map_origen[origen], distancia, map_via[tipo_via], map_clima[clima]]])
input_scaled = scaler.transform(input_data)

# Predicción
tiempo_estimado = model.predict(input_scaled)[0][0]
tiempo_estimado = round(tiempo_estimado, 2)

# Mostrar resultado
st.success(f"🕒 Tiempo estimado de entrega: {tiempo_estimado} minutos")

