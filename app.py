import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime
import pytz

# --- CONFIGURACIÓN DE CONEXIÓN ---
DATABASE_URL = "postgresql://postgres.aiiqkmslpfcleptmejfk:Brunokaliq12345@aws-0-us-east-2.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL, future=True)

# --- FUNCIONES AUXILIARES ---
@st.cache_data(ttl=600)
def get_users():
    with engine.connect() as conn:
        return pd.read_sql("SELECT * FROM users", conn)

@st.cache_data(ttl=600)
def get_orders():
    with engine.connect() as conn:
        return pd.read_sql("SELECT * FROM orders", conn)

def insert_order(user_id, origen, destino, estado, tiempo_estimado, hora_salida):
    insert_sql = text("""
        INSERT INTO orders (user_id, origen, destino, estado, tiempo_estimado_min, hora_salida)
        VALUES (:user_id, :origen, :destino, :estado, :tiempo_estimado, :hora_salida)
    """)
    with engine.begin() as conn:
        conn.execute(insert_sql, {
            "user_id": user_id,
            "origen": origen,
            "destino": destino,
            "estado": estado,
            "tiempo_estimado": tiempo_estimado,
            "hora_salida": hora_salida
        })

# --- MENÚ LATERAL ---
st.sidebar.title("Menú")
menu = ["Dashboard", "Órdenes", "Usuarios", "Agregar Pedido"]
choice = st.sidebar.radio("Ir a:", menu)

# --- DASHBOARD ---
if choice == "Dashboard":
    st.title("📊 Dashboard de Logística")
    orders_df = get_orders()
    total = len(orders_df)
    en_ruta = len(orders_df[orders_df['estado'] == "En ruta"])
    entregados = len(orders_df[orders_df['estado'] == "Entregado"])
    pend
