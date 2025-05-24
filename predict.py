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

    # ACCESO A LAS CATEGORÍAS REALES DEL ENCODER (ORDEN CORRECTO)
    dias = encoder.categories_[0]
    zonas = encoder.categories_[1]
    climas = encoder.categories_[2]
    tipos_via = encoder.categories_[3]

    # FORMULARIO
    hora = st.number_input("Hora de salida (0-23)", min_value=0, max_value=23, value=8)
    dia = st.selectbox("Día", dias)
    zona = st.selectbox("Zona", zonas)
    clima = st.selectbox("Clima", climas)
    tipo_via = st.selectbox("Tipo de vía", tipos_via)
    distancia_km = st.number_input("Distancia (km)", min_value=0.1, max_value=100.0, value=5.0, step=0.1)

    if st.button("Predecir"):
        # El input DEBE SER exactamente el orden de entrenamiento del modelo
        X_new = np.array([[dia, zona, clima, tipo_via, hora, distancia_km]], dtype=object)
        try:
            # OJO: Si el encoder fue ajustado a solo variables categóricas, separa lo numérico.
            # Si usaste ColumnTransformer, puede que encoder espere solo categóricas.
            # Supón que tu pipeline toma todo junto (lo más común en producción):
            X_encoded = encoder.transform([[dia, zona, clima, tipo_via]])
            # Agrega lo numérico al array que irá al scaler/model
            # Si tu pipeline requiere [dia, zona, clima, tipo_via, hora, distancia], ajústalo según tu entrenamiento

            # Si tu pipeline NO transforma numéricos y solo procesa categóricos,
            # concatena las features para el scaler y modelo:
            # (Aquí un ejemplo suponiendo que el encoder solo procesa las 4 categóricas)
            X_total = np.hstack([X_encoded, [[hora, distancia_km]]])

            X_scaled = scaler.transform(X_total)
            pred = model.predict(X_scaled)
            st.success(f"Tiempo estimado de entrega: {pred[0][0]:.2f} minutos")
        except Exception as e:
            st.error(f"Error en la predicción: {e}")
