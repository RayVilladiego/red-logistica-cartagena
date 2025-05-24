# about.py

import streamlit as st

def show_about():
    st.title("🛣️ Red Logística Inteligente - Cartagena")
    st.markdown("""
Esta aplicación permite estimar y visualizar en tiempo real variables clave del sistema logístico de entregas en Cartagena usando Machine Learning y mapas interactivos.

**Proyecto académico | Distribución y Transporte**  
**Profesor:** PhD. Germán Herrera Vidal  
**Universidad Tecnológica de Bolívar**  
**Desarrollado por:** Raylin Villadiego Rivero y colaboradores  
**Contacto:** villadiegor@utb.edu.co

---

#### 🔍 Funcionalidades:
- Predicción del tiempo estimado de entrega
- Visualización y edición de rutas en mapa
- Recomendación de franjas horarias según tráfico
- Alertas de congestión en tiempo real o simulada
- Exportación de datos a Excel/PDF
- Dashboard de KPIs (pedidos activos, entregados, en ruta)
- Simulación de movimiento de entregas
- Históricos para análisis posterior
- Integración preparada con API de tráfico (Mapbox, OpenRouteService)

---

#### 🧠 Tecnologías:
Streamlit, Folium/OpenStreetMap, TensorFlow/Keras, scikit-learn, pandas, joblib, numpy, matplotlib.

---

#### 📦 Estructura del proyecto:
- app.py: App principal
- modelo_entrega.h5: Red neuronal
- scaler_entrega.pkl: Scaler estándar
- columnas_modelo.pkl: Columnas de predicción
- requirements.txt: Dependencias
- README.md: Manual y guía

---

#### 🚀 Ejecución rápida:
```bash
git clone https://github.com/tuusuario/red-logistica-cartagena.git
cd red-logistica-cartagena
pip install -r requirements.txt
streamlit run app.py
