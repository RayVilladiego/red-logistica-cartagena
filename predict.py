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

    # Obtén las categorías válidas
    categorias_origen = encoder.categories_[0]
    categorias_destino = encoder.categories_[1]
    categorias_clima = encoder.categories_[2]

    origen = st.selectbox("Origen", categorias_origen)
    destino = st.selectbox("Destino", categorias_destino)
    clima = st.selectbox("Clima", categorias_clima)
    hora_salida = st.time_input("Hora de salida")  # si la hora es numérica, deja el input

    if st.button("Predecir"):
        try:
            X = np.array([[origen, destino, clima, str(hora_salida)]])
            X_encoded = encoder.transform(X)
            X_scaled = scaler.transform(X_encoded)
            pred = model.predict(X_scaled)
            st.success(f"Tiempo estimado de entrega: {pred[0][0]:.2f} minutos")
        except Exception as e:
            st.error(f"Error en la predicción: {e}")
