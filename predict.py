import streamlit as st
import numpy as np
import joblib
from tensorflow.keras.models import load_model

# --- LISTA DE ZONAS ---
zonas = [
    "Mamonal", "Bocagrande", "Centro", "Getsemaní", "El Pozón", "San Felipe", "Crespo", "Pie de la Popa",
    "Manga", "Los Alpes", "La Boquilla", "El Bosque", "El Laguito", "Otro"
]

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

    # Entradas del usuario
    origen = st.selectbox("Origen", zonas)
    destino = st.selectbox("Destino", zonas)
    hora_salida = st.time_input("Hora de salida")

    # Ajusta aquí los features según tu modelo
    if st.button("Predecir"):
        # Preprocesamiento (ajusta según lo que espere tu encoder)
        X = np.array([[origen, destino, str(hora_salida)]])
        try:
            # Codifica y escala (ajusta estos pasos según tu pipeline real)
            X_encoded = encoder.transform(X)
            X_scaled = scaler.transform(X_encoded)
            pred = model.predict(X_scaled)
            st.success(f"Tiempo estimado de entrega: {pred[0][0]:.2f} minutos")
        except Exception as e:
            st.error(f"Error en la predicción: {e}")
