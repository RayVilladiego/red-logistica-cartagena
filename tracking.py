import pandas as pd
import numpy as np
import pickle
from tensorflow.keras.models import load_model

# Rutas de los archivos del modelo y preprocesadores
MODEL_PATH = 'modelo_entrega.h5'          # Ajusta según el nombre exacto
SCALER_PATH = 'scaler_entrega.pkl'
ENCODER_PATH = 'encoder_entrega.pkl'

# Carga los objetos solo una vez
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
    # df_nuevo debe tener las columnas necesarias
    X_cat = encoder.transform(df_nuevo[categorical_cols])
    X_num = scaler.transform(df_nuevo[numerical_cols])
    X_proc = np.hstack([X_num, X_cat])
    pred = modelo.predict(X_proc)
    return pred.flatten()
