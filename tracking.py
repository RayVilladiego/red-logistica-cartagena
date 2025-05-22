import os
import pandas as pd
import numpy as np
import pickle
from tensorflow.keras.models import load_model

# Define rutas claras (ajusta si están en subcarpetas)
MODEL_PATH = 'modelo_entrega (1).h5'  # o 'modelos/modelo_entrega.h5' si está en subcarpeta
SCALER_PATH = 'scaler_entrega (1).pkl'
ENCODER_PATH = 'encoder_entrega.pkl'

# Verificar que los archivos existan
for file_path in [MODEL_PATH, SCALER_PATH, ENCODER_PATH]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró el archivo necesario: {file_path}")

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
    # Asegurarse que el df_nuevo tenga las columnas necesarias
    X_cat = encoder.transform(df_nuevo[categorical_cols])
    X_num = scaler.transform(df_nuevo[numerical_cols])
    X_proc = np.hstack([X_num, X_cat])
    pred = modelo.predict(X_proc)
    return pred.flatten()
