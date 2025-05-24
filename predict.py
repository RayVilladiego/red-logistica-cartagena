import streamlit as st
import numpy as np
import joblib
from tensorflow.keras.models import load_model

def predict_view():
    st.title("🔮 Predicción del Tiempo de Entrega")

    @st.cache_resource
    def load_models():
        model = load_model("modelo_entrega.h5")
        encoder = joblib.load("encoder_entrega.pkl")
        scaler = joblib.load("scaler_entrega.pkl")
        return model, encoder, scaler

    model, encoder, scaler = load_models()

    # Listas de categorías según encoder (orden y valores exactos)
    dias = encoder.categories_[0]
    zonas = encoder.categories_[1]
    climas = encoder.categories_[2]
    tipos_via = encoder.categories_[3]

    # Inputs del usuario
    hora = st.number_input("Hora de salida (0-23)", min_value=0, max_value=23, value=8)
    distancia_km = st.number_input("Distancia (km)", min_value=0.1, max_value=100.0, value=5.0, step=0.1)
    velocidad_prom = st.number_input("Velocidad promedio (km/h)", min_value=1, max_value=100, value=30, step=1)
    dia = st.selectbox("Día", dias)
    zona = st.selectbox("Zona", zonas)
    clima = st.selectbox("Clima", climas)
    tipo_via = st.selectbox("Tipo de vía", tipos_via)

    if st.button("Predecir"):
        # Construye la matriz de entrada respetando el orden de entrenamiento:
        # Primero variables numéricas
        X_num = np.array([[hora, distancia_km, velocidad_prom]])
        # Luego variables categóricas codificadas
        X_cat = encoder.transform([[dia, zona, clima, tipo_via]])
        # Concatenar ambas matrices horizontalmente
        X_processed = np.hstack([X_num, X_cat])

        try:
            # Escalar todo antes de predecir
            X_scaled = scaler.transform(X_processed)
            pred = model.predict(X_scaled)
            st.success(f"Tiempo estimado de entrega: {pred[0][0]:.2f} minutos")
        except Exception as e:
            st.error(f"Error en la predicción: {e}")
