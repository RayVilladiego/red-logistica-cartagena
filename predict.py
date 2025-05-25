import streamlit as st
import numpy as np
import joblib
from tensorflow.keras.models import load_model

def predict_view():
    @st.cache_resource
    def load_models():
        model = load_model("modelo_entrega.h5", compile=False)
        encoder = joblib.load("encoder_entrega.pkl")  # OneHotEncoder
        scaler = joblib.load("scaler_entrega.pkl")    # StandardScaler (ajustado a los 23 features)
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
            # Primero codifica categóricos → one-hot
            X_cat = encoder.transform([[dia, zona, clima, tipo_via]])  # shape (1, N)

            # Luego concatena los numéricos al final (igual que en tu entrenamiento)
            X_all = np.concatenate([X_cat, np.array([[hora, distancia_km, velocidad_promedio]])], axis=1)  # shape (1, 20+3=23)

            # Ahora sí, escalar TODO el array
            X_scaled = scaler.transform(X_all)  # scaler espera shape (1, 23)

            # Predicción
            pred = model.predict(X_scaled)
            st.success(f"Tiempo estimado de entrega: {pred[0][0]:.2f} minutos")
        except Exception as e:
            st.error(f"Error en la predicción: {e}")
