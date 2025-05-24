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

    # Listas fijas para diagnóstico
    dias = ['Domingo', 'Jueves', 'Lunes', 'Martes', 'Miércoles', 'Sábado', 'Viernes']
    zonas = ['Bocagrande', 'Centro', 'Getsemaní', 'La Boquilla', 'Mamonal']
    climas = ['Lluvioso', 'Nublado', 'Soleado']
    tipos_via = ['Principal', 'Secundaria', 'Terciaria']

    hora = st.number_input("Hora de salida (0-23)", min_value=0, max_value=23, value=8)
    distancia_km = st.number_input("Distancia (km)", min_value=0.1, max_value=100.0, value=5.0, step=0.1)
    velocidad_prom = st.number_input("Velocidad promedio (km/h)", min_value=1, max_value=100, value=30, step=1)

    dia = st.selectbox("Día de la semana", dias)
    st.write("Días disponibles:", dias)
    st.write("Día seleccionado:", dia)

    zona = st.selectbox("Zona Destino", zonas)
    st.write("Zonas disponibles:", zonas)
    st.write("Zona seleccionada:", zona)

    clima = st.selectbox("Clima", climas)
    st.write("Climas disponibles:", climas)
    st.write("Clima seleccionado:", clima)

    tipo_via = st.selectbox("Tipo de vía", tipos_via)
    st.write("Tipos de vía disponibles:", tipos_via)
    st.write("Tipo de vía seleccionado:", tipo_via)

    if st.button("Predecir"):
        X_cat = encoder.transform([[dia, zona, clima, tipo_via]])
        X_num = np.array([[hora, distancia_km, velocidad_prom]])
        X_processed = np.hstack([X_num, X_cat])

        try:
            X_scaled = scaler.transform(X_processed)
            pred = model.predict(X_scaled)
            st.success(f"Tiempo estimado de entrega: {pred[0][0]:.2f} minutos")
        except Exception as e:
            st.error(f"Error en la predicción: {e}")
