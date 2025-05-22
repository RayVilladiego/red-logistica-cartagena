import streamlit as st
import pandas as pd
import numpy as np
import pickle
from tensorflow.keras.models import load_model

# Archivos de modelo y preprocesadores (ajusta nombres si cambian)
MODEL_PATH = 'modelo_entrega (1).h5'
SCALER_PATH = 'scaler_entrega (1).pkl'
ENCODER_PATH = 'encoder_entrega.pkl'

@st.cache_resource(show_spinner=False)
def cargar_modelo():
    model = load_model(MODEL_PATH)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
    with open(ENCODER_PATH, 'rb') as f:
        encoder = pickle.load(f)
    return model, scaler, encoder

modelo, scaler, encoder = cargar_modelo()

categorical_cols = ['Día', 'Zona', 'Clima', 'Tipo_Via']
numerical_cols = ['Hora', 'Distancia', 'Velocidad_Promedio']

def predecir_tiempo(df_nuevo):
    X_cat = encoder.transform(df_nuevo[categorical_cols])
    X_num = scaler.transform(df_nuevo[numerical_cols])
    X_proc = np.hstack([X_num, X_cat])
    pred = modelo.predict(X_proc)
    return pred.flatten()

# --- UI Streamlit ---
st.set_page_config(page_title="🚚 Logística Cartagena", layout="wide")

st.title("🚛 Predicción de Tiempo de Entrega - Logística Cartagena")

st.markdown("""
Bienvenido al sistema de **predicción y seguimiento logístico** de entregas.  
Ingresa los datos para conocer el tiempo estimado y optimizar tu operación.  
""")

with st.form("formulario_entrada"):
    col1, col2, col3 = st.columns(3)

    with col1:
        hora = st.number_input("⏰ Hora (0-23)", min_value=0, max_value=23, value=8)
        dia = st.selectbox("📅 Día", ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'])
        zona = st.selectbox("📍 Zona", ['Mamonal', 'Getsemaní', 'Bocagrande', 'La Boquilla', 'Centro'])

    with col2:
        clima = st.selectbox("☁️ Clima", ['Soleado', 'Nublado', 'Lluvioso'])
        tipo_via = st.selectbox("🛣️ Tipo de Vía", ['Principal', 'Secundaria', 'Terciaria'])

    with col3:
        distancia = st.number_input("📏 Distancia (km)", min_value=0.1, max_value=200.0, value=10.0)
        velocidad_promedio = st.number_input("🚦 Velocidad Promedio (km/h)", min_value=10.0, max_value=100.0, value=50.0)

    submit = st.form_submit_button("Calcular Tiempo Estimado 🚀")

if submit:
    df_input = pd.DataFrame([{
        'Hora': hora,
        'Día': dia,
        'Zona': zona,
        'Clima': clima,
        'Tipo_Via': tipo_via,
        'Distancia': distancia,
        'Velocidad_Promedio': velocidad_promedio
    }])

    prediccion = predecir_tiempo(df_input)
    st.success(f"✅ Tiempo estimado de entrega: **{prediccion[0]:.2f} minutos**")
