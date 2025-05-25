import streamlit as st
import numpy as np
import joblib
import pandas as pd
from tensorflow.keras.models import load_model

def predict_view():
    @st.cache_resource
    def load_models():
        model = load_model("modelo_entrega.h5", compile=False)
        encoder = joblib.load("encoder_entrega.pkl")
        scaler = joblib.load("scaler_entrega.pkl")
        return model, encoder, scaler

    model, encoder, scaler = load_models()

    # Opciones en el mismo orden que los datos de entrenamiento
    dias = ['Domingo', 'Jueves', 'Lunes', 'Martes', 'Miércoles', 'Sábado', 'Viernes']
    zonas = ['Bocagrande', 'Centro', 'Getsemaní', 'La Boquilla', 'Mamonal']
    climas = ['Lluvioso', 'Nublado', 'Soleado']
    tipos_via = ['Principal', 'Secundaria', 'Terciaria']

    # Inputs en el mismo orden que el entrenamiento
    hora = st.number_input("Hora de salida (0-23)", min_value=0, max_value=23, value=8)
    distancia_km = st.number_input("Distancia (km)", min_value=0.1, max_value=100.0, value=5.0, step=0.1)
    velocidad_prom = st.number_input("Velocidad promedio (km/h)", min_value=1, max_value=100, value=30, step=1)
    dia = st.selectbox("Día de la semana", dias)
    zona = st.selectbox("Zona Destino", zonas)
    clima = st.selectbox("Clima", climas)
    tipo_via = st.selectbox("Tipo de vía", tipos_via)

    if st.button("Predecir"):
        try:
            # Arma DataFrame exactamente igual que en el entrenamiento
            columnas = ['Hora', 'Distancia', 'Velocidad_Promedio', 'Día', 'Zona', 'Clima', 'Tipo_Via']
            X_input = pd.DataFrame([[hora, distancia_km, velocidad_prom, dia, zona, clima, tipo_via]], columns=columnas)

            # Aplica el pipeline completo: encoder+scaler
            # Si tu encoder es ColumnTransformer, solo llama encoder.transform(X_input)
            X_encoded = encoder.transform(X_input)
            X_scaled = scaler.transform(X_encoded)
            pred = model.predict(X_scaled)
            st.success(f"Tiempo estimado de entrega: {pred[0][0]:.2f} minutos")
        except Exception as e:
            st.error(f"Error en la predicción: {e}")
