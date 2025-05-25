import streamlit as st
import numpy as np
import pandas as pd
import joblib
from tensorflow.keras.models import load_model

def predict_view():
    @st.cache_resource
    def load_models():
        model = joblib.load("modelo_entrega.h5")  # O usa load_model si es keras, pero asegúrate
        encoder = joblib.load("encoder_entrega.pkl")
        scaler = joblib.load("scaler_entrega.pkl")
        return model, encoder, scaler

    model, encoder, scaler = load_models()

    # Listas para los selects
    dias = ['Domingo', 'Jueves', 'Lunes', 'Martes', 'Miércoles', 'Sábado', 'Viernes']
    zonas = ['Bocagrande', 'Centro', 'Getsemaní', 'La Boquilla', 'Mamonal']
    climas = ['Lluvioso', 'Nublado', 'Soleado']
    tipos_via = ['Principal', 'Secundaria', 'Terciaria']

    # Inputs de usuario
    hora = st.number_input("Hora de salida (0-23)", min_value=0, max_value=23, value=8)
    distancia_km = st.number_input("Distancia (km)", min_value=0.1, max_value=100.0, value=5.0, step=0.1)
    dia = st.selectbox("Día de la semana", dias)
    zona = st.selectbox("Zona Destino", zonas)
    clima = st.selectbox("Clima", climas)
    tipo_via = st.selectbox("Tipo de vía", tipos_via)

    # DataFrame con nombres y orden EXACTOS
    columnas = ['distancia_km', 'hora', 'dia_semana', 'zona_destino', 'clima', 'tipo_via']
    X_input = pd.DataFrame([[distancia_km, hora, dia, zona, clima, tipo_via]], columns=columnas)

    if st.button("Predecir"):
        try:
            # Si tu modelo es sklearn pipeline (no keras)
            pred = model.predict(X_input)
            st.success(f"Tiempo estimado de entrega: {pred[0]:.2f} minutos")
        except Exception as e:
            st.error(f"Error en la predicción: {e}")
