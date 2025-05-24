import streamlit as st
import numpy as np
import joblib
from tensorflow.keras.models import load_model

def predict_view():
    st.title("🔮 Predicción del Tiempo de Entrega")

    # Cargar los modelos SOLO UNA VEZ
    @st.cache_resource
    def load_models():
        model = load_model("modelo_entrega.h5")
        encoder = joblib.load("encoder_entrega.pkl")
        scaler = joblib.load("scaler_entrega.pkl")
        return model, encoder, scaler

    model, encoder, scaler = load_models()

    # Cargar las categorías válidas directamente del encoder
    categorias_origen = encoder.categories_[0]
    categorias_destino = encoder.categories_[1]
    categorias_hora = encoder.categories_[2]
    categorias_clima = encoder.categories_[3]

    # Solo muestra los valores válidos
    origen = st.selectbox("Zona Origen", categorias_origen)
    destino = st.selectbox("Zona Destino", categorias_destino)
    hora_salida = st.selectbox("Hora de salida (hh:mm)", categorias_hora)
    clima = st.selectbox("Clima", categorias_clima)

    if st.button("Predecir"):
        X = np.array([[origen, destino, hora_salida, clima]])
        try:
            X_encoded = encoder.transform(X)
            X_scaled = scaler.transform(X_encoded)
            pred = model.predict(X_scaled)
            st.success(f"Tiempo estimado de entrega: {pred[0][0]:.2f} minutos")
        except Exception as e:
            st.error(f"Error en la predicción: {e}")
