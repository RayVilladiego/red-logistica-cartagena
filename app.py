import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime
import pytz

# --- Configuración de la conexión ---
DATABASE_URL = "postgresql://postgres.aiiqkmslpfcleptmejfk:Brunokaliq12345@aws-0-us-east-2.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL, future=True)

# --- Inicialización segura del estado ---
if "pedido_agregado" not in st.session_state:
    st.session_state.pedido_agregado = False

# --- Funciones para obtener datos ---
@st.cache_data(ttl=600)
def get_users():
    try:
        with engine.connect() as conn:
            return pd.read_sql("SELECT * FROM users", conn)
    except Exception as e:
        st.error(f"Error cargando usuarios: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=600)
def get_orders():
    try:
        with engine.connect() as conn:
            return pd.read_sql("SELECT * FROM orders", conn)
    except Exception as e:
        st.error(f"Error cargando órdenes: {e}")
        return pd.DataFrame()

def insert_order(user_id, origen, destino, estado, tiempo_estimado, hora_salida):
    try:
        insert_sql = text("""
            INSERT INTO orders (user_id, origen, destino, estado, tiempo_esti
