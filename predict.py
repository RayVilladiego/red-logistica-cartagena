import streamlit as st
import joblib
import numpy as np

def predict_view():
    st.title("🔮 Predicción del Tiempo de Entrega")

    # Cargar los modelos entrenados SOLO UNA VEZ
    @st.cache_resource
    def load_models():
        model = joblib.load("modelo_entrega.h5")
        encoder = joblib.load("encoder_entrega.pkl")
        scaler = joblib.load("scaler_entrega.pkl")
        return model, encoder, scaler

    model, encoder, scaler = load_models()

    # Entradas del usuario
    origen = st.text_input("Origen")
    destino = st.text_input("Destino")
    hora_salida = st.time_input("Hora de salida")

    # ... Puedes pedir otros campos requeridos por tu modelo ...

    if st.button("Predecir"):
        # Preprocesar datos de entrada
        X = np.array([[origen, destino, str(hora_salida)]])  # Ajústalo según tus features

        # Ejemplo de pipeline (ajusta a tu flujo real):
        # X_encoded = encoder.transform(X)
        # X_scaled = scaler.transform(X_encoded)
        # pred = model.predict(X_scaled)
        # st.success(f"Tiempo estimado: {pred[0]} minutos")

        st.info("Aquí va la predicción real con tu modelo")
