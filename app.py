import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime
import pytz

# --- CONFIGURACIÓN DE CONEXIÓN ---
DATABASE_URL = "postgresql://postgres.aiiqkmslpfcleptmejfk:Brunokaliq12345@aws-0-us-east-2.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL)

# --- Inicializar variable en session_state ---
if "pedido_agregado" not in st.session_state:
    st.session_state.pedido_agregado = False

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
