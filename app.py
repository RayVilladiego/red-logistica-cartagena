import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime
import pytz

# --- Configuración de conexión ---
DATABASE_URL = "postgresql://postgres.aiiqkmslpfcleptmejfk:Brunokaliq12345@aws-0-us-east-2.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL, future=True)

# --- Inicializar estado ---
if "pedido_agregado" not in st.session_state:
    st.session_state.pedido_agregado = False

# --- Funciones auxiliares sin caché para debug ---
def get_users():
    try:
        with engine.connect() as conn:
            df = pd.read_sql("SELECT * FROM users", conn)
            return df
    except Exception as e:
        st.error(f"Error cargando usuarios: {e}")
        return pd.DataFrame()

def get_orders():
    try:
        with engine.connect() as conn:
            df = pd.read_sql("SELECT * FROM orders", conn)
            return df
    except Exception as e:
        st.error(f"Error cargando órdenes: {e}")
        return pd.DataFrame()

def insert_order(user_id, origen, destino, estado, tiempo_estimado, hora_salida):
    try:
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
        return True, None
    except Exception as e:
        return False, str(e)

# --- Mensajes de debug al inicio ---
st.write("🚀 La app arrancó correctamente")

users_df = get_users()
st.write(f"Usuarios cargados: {len(users_df)}")

orders_df = get_orders()
st.write(f"Órdenes cargadas
