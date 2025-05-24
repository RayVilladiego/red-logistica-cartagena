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

    # Opciones (pon aquí tus zonas reales)
    zonas = [
        "Cartagena", "Centro de Cartagena", "Mamonal", "Crespo", "Getsemaní", "Bocagrande",
        "Manga", "Pie de la Popa", "La Boquilla", "El Bosque"
    ]
    climas = ["Soleado", "Nublado", "Lluvioso", "Tormenta"]  # Cambia según tus categorías reales

    # Entradas del usuario
    origen = st.selectbox("Zona Origen", zonas)
    destino = st.selectbox("Zona Destino", zonas)
    hora_salida = st.text_input("Hora de salida (hh:mm)", value="08:00")
    clima = st.selectbox("Clima", climas)

    # Formatear la entrada para el encoder (debe tener 4 campos en el orden correcto)
    if st.button("Predecir"):
        try:
            X = np.array([[origen, destino, hora_salida, clima]])
            X_encoded = encoder.transform(X)
            X_scaled = scaler.transform(X_encoded)
            pred = model.predict(X_scaled)
            st.success(f"Tiempo estimado de entrega: {pred[0][0]:.2f} minutos")
        except Exception as e:
            st.error(f"Error en la predicción: {e}")
