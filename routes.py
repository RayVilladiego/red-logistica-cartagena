import streamlit as st
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from database import get_route_data

# Cargar modelo y escalador
model = load_model("modelo_entrega.h5")
scaler = joblib.load("scaler_entrega.pkl")

# Velocidad promedio por hora del día en Cartagena (km/h)
velocidad_por_hora = {
    0: 35, 1: 35, 2: 35, 3: 35, 4: 35,
    5: 15, 6: 15,
    7: 25, 8: 25,
    9: 30, 10: 30, 11: 30,
    12: 18, 13: 18,
    14: 30, 15: 30, 16: 30,
    17: 16, 18: 16,
    19: 28, 20: 28, 21: 28, 22: 28, 23: 28
}

def predict_time(input_data, distancia, hora):
    try:
        df_input = input_data.copy()
        df_scaled = scaler.transform(df_input)
        prediction = model.predict(df_scaled)[0][0]
        if prediction < 3 or prediction > 180:
            raise ValueError("Predicción fuera de rango")
        return prediction
    except:
        velocidad = velocidad_por_hora.get(hora, 30)
        return (distancia / velocidad) * 60  # tiempo en minutos

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
    pred = predict_time(entrada_array, distancia, hora)

    st.success(f"⏱ Tiempo estimado de entrega: {round(pred, 2)} minutos")

    if hora < 5 or hora > 19:
        st.warning("⚠️ Franja no recomendada. Posibles riesgos por oscuridad o congestión.")
    elif hora in [5, 6, 12, 13, 17, 18]:
        st.warning("⚠️ Horario con alta congestión o tráfico por movilidad laboral o estudiantil.")
    else:
        st.info("✅ Franja óptima para entregar.")
