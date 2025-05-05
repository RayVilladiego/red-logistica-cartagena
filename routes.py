import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
import joblib
from database import get_route_data

# Cargar modelo, escalador y columnas en el mismo orden
model = load_model("modelo_entrega.h5", compile=False)
scaler = joblib.load("scaler_entrega.pkl")
columnas = joblib.load("columnas_modelo.pkl")  # <- Carga las columnas esperadas

def predict_time(input_dict):
    # Convertir diccionario a array en el mismo orden que se usó para entrenar
    input_ordered = np.array([[input_dict[col] for col in columnas]])
    scaled = scaler.transform(input_ordered)
    prediction = model.predict(scaled)[0][0]
    return prediction

def show_route():
    st.subheader("🛣️ Predicción de Ruta Inteligente")
    route_data = get_route_data()
    st.write("Rutas actuales:")
    st.dataframe(route_data)

    distancia = st.slider("📏 Distancia (km)", 1.0, 100.0, 8.0)
    hora = st.slider("🕓 Hora de salida", 0, 23, 10)
    clima = st.selectbox("🌦 Clima actual", ["Soleado", "Nublado", "Lluvioso"])

    clima_vec = {
        "Clima_Lluvioso": int(clima == "Lluvioso"),
        "Clima_Nublado": int(clima == "Nublado"),
        "Clima_Soleado": int(clima == "Soleado")
    }

    entrada = {
        "Distancia": distancia,
        "Hora": hora,
        **clima_vec
    }

    try:
        pred = predict_time(entrada)
        st.success(f"⏱ Tiempo estimado de entrega: {round(pred, 2)} minutos")
        if hora < 7 or hora > 19:
            st.warning("⚠️ Franja no recomendada. Riesgo de congestión o poca visibilidad.")
        else:
            st.info("✅ Franja óptima para entregar.")
    except Exception as e:
        st.error(f"Error en la predicción: {e}")
