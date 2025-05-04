import streamlit as st
import numpy as np
import pandas as pd
import joblib
from tensorflow.keras.models import load_model

# Cargar modelos
model = load_model("modelo_entrega.h5")
scaler = joblib.load("scaler_entrega.pkl")
columnas_modelo = joblib.load("columnas_modelo.pkl")

# Interfaz de usuario
st.title("Predicción de Tiempo de Entrega en Cartagena")

zona_origen = st.selectbox("Zona de origen", ["CDI1", "CDI2"])
zona_destino = st.selectbox("Zona de destino", ["Retail1", "Retail2", "Tienda3", "Almacén4", "Puerto5"])
hora_dia = st.slider("Hora del día", 0, 23, 12)
dia_semana = st.slider("Día de la semana", 1, 7, 3)
distancia_km = st.slider("Distancia (km)", 2.0, 30.0, 10.0)
tipo_via = st.selectbox("Tipo de vía", ["Secundaria", "Principal", "Interbarrial"])
clima = st.selectbox("Clima", ["Soleado", "Lluvia", "Nublado"])

# Crear input para el modelo
input_data = pd.DataFrame([{
    "hora_dia": hora_dia,
    "dia_semana": dia_semana,
    "distancia_km": distancia_km,
    "zona_origen": zona_origen,
    "zona_destino": zona_destino,
    "tipo_via": tipo_via,
    "clima": clima
}])
input_data = pd.get_dummies(input_data)
for col in columnas_modelo:
    if col not in input_data.columns:
        input_data[col] = 0
input_data = input_data[columnas_modelo]

# Escalar y predecir
input_scaled = scaler.transform(input_data)
prediccion = model.predict(input_scaled)

# Resultado
st.success(f"Tiempo estimado de entrega: {prediccion[0][0]:.2f} minutos")