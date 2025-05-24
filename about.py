import streamlit as st

def show_about():
    st.markdown("""
    # 🛣️ Red Logística Inteligente - Cartagena

    ### Distribución y Transporte  
    **Profesor:** Germán Herrera Vidal  
    **Universidad Tecnológica de Bolívar**

    ---

    Esta aplicación permite estimar y visualizar en tiempo real variables clave del sistema logístico de entregas en la ciudad de Cartagena usando Machine Learning y mapas interactivos.

    ### 🔍 Funcionalidades destacadas
    - ✅ Predicción del tiempo estimado de entrega (en minutos)
    - ✅ Visualización de rutas en mapa editable (selección manual de origen/destino)
    - ✅ Recomendación de la mejor franja horaria para salir según el tráfico
    - ✅ Alerta de zonas con mayor congestión (simulada o en tiempo real)
    - ✅ Exportación de rutas y entregas en Excel o PDF
    - ✅ Dashboard con KPIs de seguimiento: pedidos activos, entregados, y en ruta
    - ✅ Simulación de movimiento de entregas con seguimiento visual
    - ✅ Base de datos con históricos para análisis posterior
    - ✅ Preparado para conexión con API de tráfico (Mapbox, OpenRouteService)

    ### 🧠 Tecnologías
    Streamlit para interfaz interactiva  
    Folium + OpenStreetMap para visualización de rutas  
    Tensorflow/Keras para el modelo predictivo  
    scikit-learn para el escalado de datos  
    pandas, joblib, numpy, matplotlib y más

    ---
    **Proyecto académico desarrollado por Raylin Villadiego Rivero y colaboradores.  
    👨‍💻 Contacto: villadiegor@utb.edu.co**
    """)
