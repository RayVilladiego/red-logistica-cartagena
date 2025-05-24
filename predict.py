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

    # Acceso robusto a las categorías
    if hasattr(encoder, 'transformers_'):
        categorias_zona_destino = encoder.transformers_[0][1].categories_[0]
        categorias_clima = encoder.transformers_[0][1].categories_[1]
        categorias_tipo_via = encoder.transformers_[0][1].categories_[2]
    elif hasattr(encoder, 'transformers'):
        categorias_zona_destino = encoder.transformers[0][1].categories_[0]
        categorias_clima = encoder.transformers[0][1].categories_[1]
        categorias_tipo_via = encoder.transformers[0][1].categories_[2]
    else:
        st.error("No se pudieron encontrar las categorías en el encoder.")
        return

    hora = st.number_input("Hora de salida (0-23)", min_value=0, max_value=23, value=8)
    dia_semana = st.selectbox(
        "Día de la semana",
        options=[0,1,2,3,4,5,6],
        format_func=lambda x: ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"][x]
    )
    zona_destino = st.selectbox("Zona Destino", categorias_zona_destino)
    clima = st.selectbox("Clima", categorias_clima)
    tipo_via = st.selectbox("Tipo de vía", categorias_tipo_via)
    distancia_km = st.number_input("Distancia (km)", min_value=0.1, max_value=100.0, value=5.0, step=0.1)

    if st.button("Predecir"):
        X_new = np.array([[hora, dia_semana, zona_destino, clima, tipo_via, distancia_km]])
        try:
            X_encoded = encoder.transform(X_new)
            X_scaled = scaler.transform(X_encoded)
            pred = model.predict(X_scaled)
            st.success(f"Tiempo estimado de entrega: {pred[0][0]:.2f} minutos")
        except Exception as e:
            st.error(f"Error en la predicción: {e}")
