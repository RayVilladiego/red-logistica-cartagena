# Extrae correctamente las categorías del encoder
if hasattr(encoder, 'transformers_'):
    categorias_zona_destino = encoder.transformers_[0][1].categories_[0]
    categorias_clima = encoder.transformers_[0][1].categories_[1]
    categorias_tipo_via = encoder.transformers_[0][1].categories_[2]
else:
    categorias_zona_destino = encoder.categories_[0]
    categorias_clima = encoder.categories_[1]
    categorias_tipo_via = encoder.categories_[2]

# Formulario: cada selectbox va con su lista correcta
hora = st.number_input("Hora de salida (0-23)", min_value=0, max_value=23, value=8)
dia_semana = st.selectbox(
    "Día de la semana",
    options=[0,1,2,3,4,5,6],
    format_func=lambda x: ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"][x]
)
zona_destino = st.selectbox("Zona Destino", categorias_zona_destino)
clima = st.selectbox("Clima", categorias_clima)
tipo_via = st.selectbox("Tipo de vía", categorias_tipo_via)
distancia_km = st.number_input("Distancia (km)", min_value=0.1, max_value=100.0, value=5.0, step=0.1)
