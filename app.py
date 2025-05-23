import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime
import pytz

# --- CONFIGURACIÓN DE CONEXIÓN ---
DATABASE_URL = "postgresql://postgres.aiiqkmslpfcleptmejfk:Brunokaliq12345@aws-0-us-east-2.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL)

# --- FUNCIONES AUXILIARES ---
@st.cache_data(ttl=600)
def get_users():
    return pd.read_sql("SELECT * FROM users", engine)

@st.cache_data(ttl=600)
def get_orders():
    return pd.read_sql("SELECT * FROM orders", engine)

def insert_order(user_id, origen, destino, estado, tiempo_estimado, hora_salida):
    try:
        with engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO orders (user_id, origen, destino, estado, tiempo_estimado_min, hora_salida)
                    VALUES (:user_id, :origen, :destino, :estado, :tiempo_estimado, :hora_salida)
                """),
                {
                    "user_id": user_id,
                    "origen": origen,
                    "destino": destino,
                    "estado": estado,
                    "tiempo_estimado": tiempo_estimado,
                    "hora_salida": hora_salida
                }
            )
        return True, None
    except Exception as e:
        return False, str(e)

# --- MENÚ LATERAL ---
st.sidebar.title("Menú")
menu = ["Dashboard", "Órdenes", "Usuarios", "Agregar Pedido"]
choice = st.sidebar.radio("Ir a:", menu)

# --- DASHBOARD ---
if choice == "Dashboard":
    st.title("📊 Dashboard de Logística")
    orders = get_orders()
    total = len(orders)
    en_ruta = len(orders[orders['estado'] == "En ruta"])
    entregados = len(orders[orders['estado'] == "Entregado"])
    pendientes = len(orders[orders['estado'] == "Pendiente"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Pedidos", total)
    col2.metric("Pendientes", pendientes)
    col3.metric("En Ruta", en_ruta)
    col4.metric("Entregados", entregados)
    
    st.subheader("Vista rápida de pedidos")
    st.dataframe(orders)

# --- ÓRDENES ---
elif choice == "Órdenes":
    st.title("📦 Órdenes Registradas")
    orders = get_orders()
    st.dataframe(orders)
    
# --- USUARIOS ---
elif choice == "Usuarios":
    st.title("👤 Usuarios Registrados")
    users = get_users()
    st.dataframe(users)
    
# --- AGREGAR PEDIDO ---
elif choice == "Agregar Pedido":
    st.title("➕ Agregar nuevo pedido")
    users = get_users()
    user_id = st.selectbox("Usuario", users["id"].tolist())
    origen = st.text_input("Origen")
    destino = st.text_input("Destino")
    estado = st.selectbox("Estado", ["Pendiente", "En ruta", "Entregado"])
    tiempo_estimado = st.number_input("Tiempo estimado (min)", min_value=1)
    
    # Ajustar hora a zona horaria local (ejemplo Bogotá)
    colombia_tz = pytz.timezone('America/Bogota')
    hora_salida_raw = st.time_input("Hora de salida", value=datetime.now(colombia_tz).time())
    hora_salida = datetime.combine(datetime.now(colombia_tz).date(), hora_salida_raw)
    
    # Estado para evitar doble inserción
    if 'pedido_agregado' not in st.session_state:
        st.session_state.pedido_agregado = False
    
    if st.button("Registrar Pedido"):
        if not st.session_state.pedido_agregado:
            success, error_msg = insert_order(user_id, origen, destino, estado, tiempo_estimado, hora_salida)
            if success:
                st.success("Pedido agregado correctamente")
                st.session_state.pedido_agregado = True
            else:
                st.error(f"Error al agregar pedido: {error_msg}")
        else:
            st.warning("El pedido ya fue registrado. Para agregar otro, recarga la página.")
