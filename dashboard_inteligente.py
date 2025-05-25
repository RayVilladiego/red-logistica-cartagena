import streamlit as st

def show_dashboard():
    # --- PANEL DE ALERTAS ---
    st.markdown("## 🚨 **Alertas Logísticas Inteligentes**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.error("### 🏙️ Zona Crítica\nGetsemaní\n**116 min promedio**", icon="🚦")
    with col2:
        st.warning("### 🌧️ Clima Peligroso\nLluvioso incrementa 40% el tiempo", icon="☔")
    with col3:
        st.error("### 🕒 Hora Pico\nEvita las 17:00 y 07:00", icon="⛔")

    # --- RECOMENDACIONES ---
    st.markdown("## ✅ **Recomendaciones Inteligentes**")
    col4, col5 = st.columns(2)
    with col4:
        st.success("#### 🕐 Mejor horario para despachar\n22:00, 02:00, 05:00 y 08:00", icon="⏰")
    with col5:
        st.info("#### 📆 Mejores días\nSábado y Jueves", icon="📅")

    # --- GRÁFICAS DINÁMICAS ---
    st.markdown("## 📊 **Visualización de Congestión**")
    st.write("### Tiempo promedio de entrega por zona")
    st.bar_chart({
        'Getsemaní': 116,
        'Centro': 104,
        'Mamonal': 103,
        'La Boquilla': 89,
        'Bocagrande': 82
    })

    st.write("### Tiempo promedio de entrega por hora")
    hora_dict = {
        22: 40, 2: 54, 5: 59, 8: 61, 16: 66, 23: 69, 10: 72, 4: 73, 11: 74, 15: 75,
        3: 88, 0: 88, 20: 90, 1: 91, 9: 97, 13: 98, 21: 109, 12: 111, 14: 115,
        19: 122, 18: 134, 6: 155, 7: 176, 17: 230
    }
    st.line_chart(hora_dict)

    st.write("### Impacto del clima")
    st.bar_chart({'Lluvioso': 125, 'Nublado': 90, 'Soleado': 89})

    st.write("### Impacto del día de la semana")
    st.bar_chart({'Miércoles': 127, 'Domingo': 106, 'Martes': 104, 'Viernes': 103, 'Lunes': 97, 'Jueves': 85, 'Sábado': 74})

    # --- MENSAJE FINAL ---
    st.markdown("""
    ---
    💡 **Tips finales:**  
    - Prioriza envíos en zonas y horarios de menor congestión.
    - Consulta las alertas en tiempo real antes de despachar.
    - Ante lluvia, planifica tiempos adicionales y comunica al cliente posibles demoras.
    """)
