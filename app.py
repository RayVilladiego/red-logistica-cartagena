import streamlit as st
import numpy as np
import pandas as pd
import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
import matplotlib.pyplot as plt

# Configuración de página
st.set_page_config(page_title="Red Logística Cartagena", layout="wide")

# Sidebar informativa
with st.sidebar:
    st.markdown("## 🚚 Red Logística")
    st.markdown(
        """
        Esta aplicación predice el **tiempo estimado de entrega** de productos en Cartagena,
        considerando distancia, tipo de vía y clima.

        **Desarrollado por Will Andrés Herazo**

        🔬 Proyecto académico con redes neuronales y aprendizaje automático.
        """
    )
    st.image("mapa_logistico.png", use_column_width=True)

# Encabezado
st.title("🧠 Estimador Logístico Cartagena")
st.write("Complete los datos para estimar el tiempo de entrega:")

# Inputs
origen = st.selectbox("Origen", ["Retail1", "Retail2", "Tienda3", "Almacén4", "Puerto5"])
distancia = st.slider("Distancia (km)", 2.0, 30.0, 10.0)
tipo_via = st.selectbox("Tipo de vía", ["Principal", "Secundaria"])
clima = st.selectbox("Clima", ["Soleado", "Lluvia", "Tormenta"])

# Preprocesamiento
input_data = pd.DataFrame({
    "Distancia": [distancia],
    "Tipo_via": [1 if tipo_via == "Principal" else 0],
    "Clima": [0 if clima == "Soleado" else 1 if clima == "Lluvia" else 2],
    "Puerto": [1 if origen == "Puerto5" else 0]
})

# Cargar modelos
@st.cache_resource
def cargar_modelos():
    model = load_model("modelo_entrega.h5", custom_objects={"mse": MeanSquaredError()})
    scaler = joblib.load("scaler_entrega.pkl")
    return model, scaler

model, scaler = cargar_modelos()

# Transformar y predecir
try:
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)
    tiempo = round(prediction[0][0], 2)
    st.success(f"🕒 Tiempo estimado de entrega: {tiempo} minutos")
except Exception as e:
    st.error(f"Error al realizar la predicción: {e}")
