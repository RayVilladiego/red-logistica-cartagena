import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE CONEXIÓN ---
postgresql://postgres.aiiqkmslpfcleptmejfk:Brunokaliq12345@aws-0-us-west-1.pooler.supabase.com:6543/postgres
engine = create_engine(DATABASE_URL)

# --- FUNCIONES AUXILIARES ---
@st.cache_data
def get_users():
    return pd.read_sql("SELECT * FROM users", engine)

@st.cache_data
def get_orders():
    return pd.read_sql("SELECT * FROM orders", engine)

def insert_order(user_id, origen, destino, estado, tiempo_estimado, hora_salida):
    with engine.begin() as conn:
        conn.execute(
            """
            INSERT INTO orders (user_id, origen, destino, estado, tiempo_estimado_min, hora_salida)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (user_id, origen, destino, estado, tiempo_estimado, hora_salida)
        )

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
    hora_salida = st.time_input("Hora de salida", value=datetime.now().time())

    if st.button("Registrar Pedido"):
        insert_order(user_id, origen, destino, estado, tiempo_estimado, datetime.combine(datetime.now().date(), hora_salida))
        st.success("Pedido agregado correctamente")
        st.experimental_rerun()  # Recarga la app para ver cambios

