# 🛣️ Red Logística Inteligente - Cartagena

Esta aplicación permite estimar y visualizar en tiempo real variables clave del sistema logístico de entregas en la ciudad de Cartagena usando Machine Learning y mapas interactivos.

## 🔍 Funcionalidades destacadas

✅ Predicción del tiempo estimado de entrega (en minutos)  
✅ Visualización de rutas en mapa editable (selección manual de origen/destino)  
✅ Recomendación de la mejor franja horaria para salir según el tráfico  
✅ Alerta de zonas con mayor congestión (simulada o en tiempo real)  
✅ Exportación de rutas y entregas en Excel o PDF  
✅ Dashboard con KPIs de seguimiento: pedidos activos, entregados, y en ruta  
✅ Simulación de movimiento de entregas con seguimiento visual  
✅ Base de datos con históricos para análisis posterior  
✅ Preparado para conexión con API de tráfico (Mapbox, OpenRouteService)

## 🧠 Tecnologías

- `Streamlit` para interfaz interactiva
- `Folium` + `OpenStreetMap` para visualización de rutas
- `Tensorflow/Keras` para el modelo predictivo
- `scikit-learn` para el escalado de datos
- `pandas`, `joblib`, `numpy`, `matplotlib` y más

## 📦 Estructura del proyecto

```
📁 red-logistica-cartagena/
│
├── app.py                  # Aplicación principal Streamlit
├── modelo_entrega.h5       # Red neuronal entrenada
├── scaler_entrega.pkl      # Scaler estándar para entradas
├── columnas_modelo.pkl     # Columnas utilizadas para predicción
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Este archivo 😄
```

## 🚀 Cómo ejecutarlo

1. Clona el repositorio:  
```bash
git clone https://github.com/tuusuario/red-logistica-cartagena.git
cd red-logistica-cartagena
```

2. Instala las dependencias:  
```bash
pip install -r requirements.txt
```

3. Ejecuta la aplicación:  
```bash
streamlit run app.py
```

---

📍 Proyecto académico desarrollado por **Will Andrés Herazo** y colaboradores.  
👨‍💻 Contacto: willandresh@ejemplo.com

