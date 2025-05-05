import streamlit as st
import datetime
import numpy as np
from tensorflow.keras.models import load_model
import joblib
from database import get_route_data

# Carga los modelos desde la raíz del proyecto
model = load_model("modelo_entregas.h5")
scaler = joblib.load("scaler_entrega.pkl")

def predict_time(input_data):
    df_input = input_data.copy()
    df_scaled = scaler.transform(df_input)
    prediction = model.predict(df_scaled)[0][0]
    return prediction

def show_route():
    st.subheader("🛣️ Predicción de Ruta")

    route_data = get_route_data()
    st.write("📋 Rutas actuales:")
    st.dataframe(route_data)

    distancia = st.slider("📏 Distancia estimada (km)", 1.0, 100.0, 10.0)
    hora = st.slider("🕓 Hora de salida", 0, 23, 9)
    clima = st.selectbox("☁️ Condiciones climáticas", ["Soleado", "Nublado", "Lluvioso"])

    clima_onehot = {
        "Clima_Lluvioso": int(clima == "Lluvioso"),
        "Clima_Nublado": int(clima == "Nublado"),
        "Clima_Soleado": int(clima == "Soleado")
    }

    entrada = {
        "Distancia": distancia,
        "Hora": hora,
        **clima_onehot
    }

    prediccion = predict_time(np.array([list(entrada.values())]))

    st.success(f"⏱️ Tiempo estimado de entrega: {round(prediccion, 2)} minutos")
    
    if hora < 6 or hora > 18:
        st.warning("⚠️ Evite salir en horas nocturnas por seguridad.")
    else:
        st.info("✅ Buen horario para la entrega.")
