import streamlit as st
import datetime
import numpy as np
from tensorflow.keras.models import load_model
import joblib
from database import get_route_data

model = load_model("models/modelo_entregas.h5")
scaler = joblib.load("models/escalador.pkl")

def predict_time(input_data):
    df_scaled = scaler.transform(input_data)
    pred = model.predict(df_scaled)[0][0]
    return pred

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

    entrada_array = np.array([list(entrada.values())])
    pred = predict_time(entrada_array)
    st.success(f"⏱ Tiempo estimado de entrega: {round(pred, 2)} minutos")

    if hora < 7 or hora > 19:
        st.warning("⚠️ Franja no recomendada. Riesgo de congestión o poca visibilidad.")
    else:
        st.info("✅ Franja óptima para entregar.")
