import streamlit as st
import numpy as np
import joblib
from tensorflow.keras.models import load_model

def predict_view():
    @st.cache_resource
    def load_models():
        model = load_model("modelo_entrega.h5", compile=False)
        encoder = joblib.load("encoder_entrega.pkl")
        scaler = joblib.load("scaler_entrega.pkl")
        return model, encoder, scaler

    model, encoder, scaler = load_models()

    dias = ['Domingo', 'Jueves', 'Lunes', 'Martes', 'Miércoles', 'Sábado', 'Viernes']
    zonas = ['Bocagrande', 'Centro', 'Getsemaní', 'La Boquilla', 'Mamonal']
    climas = ['Lluvioso', 'Nublado', 'Soleado']
    tipos_via = ['Principal', 'Secundaria', 'Terciaria']

    hora = st.number_input("Hora de salida (0-23)", min_value=0, max_value=23, value=8)
    distancia_km = st.number_input("Distancia (km)", min_value=0.1, max_value=100.0, value=5.0, step=0.1)
    velocidad_promedio = st.number_input("Velocidad Promedio (km/h)", min_value=1.0, max_value=200.0, value=30.0, step=0.1)
    dia = st.selectbox("Día de la semana", dias)
    zona = st.selectbox("Zona Destino", zonas)
    clima = st.selectbox("Clima", climas)
    tipo_via = st.selectbox("Tipo de vía", tipos_via)

    if st.button("Predecir"):
        try:
            # Preparar datos numéricos
            X_num = np.array([[hora, distancia_km, velocidad_promedio]])  # shape: (1, 3)

            # Codificar las variables categóricas
            X_cat = encoder.transform([[dia, zona, clima, tipo_via]])  # shape: (1, N)

            # Concatenar todo en un solo array
            X_all = np.concatenate([X_num, X_cat], axis=1)

            # Predicción
            pred = model.predict(X_all)
            st.success(f"Tiempo estimado de entrega: {pred[0][0]:.2f} minutos")
        except Exception as e:
            st.error(f"Error en la predicción: {e}")
