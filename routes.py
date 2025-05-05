import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
import joblib
from database import get_route_data

# Cargar modelo y escalador desde el mismo directorio del proyecto
model = load_model("modelo_entrega.h5", compile=False)
scaler = joblib.load("scaler_entrega.pkl")
columnas_modelo = joblib.load("columnas_modelo.pkl")

def predict_time(input_data):
    df_input = input_data.copy()
    df_scaled = scaler.transform(df_input)
    prediction = model.predict(df_scaled)[0][0]
    return prediction

def show_route():
    st.subheader("🛣️ Predicción de Ruta Inteligente")
    route_data = get_route_data()
    st.write("Rutas actuales:")
    st.dataframe(route_data)

    distancia = st.slider("📏 Distancia (km)", 1.0, 100.0, 8.0)
    hora = st.slider("🕓 Hora de salida (formato 24h)", 0, 23, 10)
    clima = st.selectbox("🌦 Clima actual", ["Soleado", "Nublado", "Lluvioso"])

    clima_vec = {
        "Clima_Lluvioso": int(clima == "Lluvioso"),
        "Clima_Nublado": int(clima == "Nublado"),
        "Clima_Soleado": int(clima == "Soleado")
    }

    # Crear diccionario con nombres exactos según el modelo
    entrada = {
        "Distancia_km": distancia,
        "hora_dia": hora,
        **clima_vec
    }

    # Asegurar orden correcto de columnas
    entrada_ordenada = np.array([[entrada[col] if col in entrada else 0 for col in columnas_modelo]])

    try:
        pred = predict_time(entrada_ordenada)
        st.success(f"⏱ Tiempo estimado de entrega: {round(pred, 2)} minutos")

        if hora < 7 or hora > 19:
            st.warning("⚠️ Franja no recomendada. Riesgo de congestión o poca visibilidad.")
        else:
            st.info("✅ Franja óptima para entregar.")
    except Exception as e:
        st.error(f"Error en la predicción: {e}")
