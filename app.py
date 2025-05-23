import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime, time
import pytz

# --- CONFIGURACIÓN DE CONEXIÓN ---
DATABASE_URL = "postgresql://postgres.aiiqkmslpfcleptmejfk:Brunokaliq12345@aws-0-us-east-2.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL, future=True)

# --- FUNCIONES AUXILIARES ---
@st.cache_data(ttl=600)
def get_users():
    query = "SELECT * FROM users"
    with engine.connect() as conn:
        return pd.read_sql(query, conn)

@st.cache_data(ttl=600)
def get_orders():
    query = "SELECT * FROM orders"
    with engine.connect() as conn:
        return pd.read_sql(query, conn)

def insert_order(user_id, origen, destino, estado, tiempo_estimado, hora_salida):
    # Convertir hora_salida a UTC para evitar problemas de zona horaria en la BD
    if isinstance(hora_salida, datetime):
        # Convertir a aware datetime con timezone local y luego a UTC
        local_tz = pytz.timezone("America/Bogota")  # Ajusta si es otra zona horaria
        aware_dt = local_tz.localize(hora_salida) if hora_salida.tzinfo is None else hora_salida
        hora_salida_utc = aware_dt.astimezone(pytz.UTC)
    else:
        # Si es time, combinar con fecha actual y luego igual que arriba
        local_tz = pytz.timezone("America/Bogota")
        dt = datetime.combine(datetime.now().date(), hora_salida)
        aware_dt = local_tz.localize(dt)
        hora_salida_utc = aware_dt.astimezone(pytz.UTC)

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
            "hora_salida": hora_salida_utc
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
    pendientes = len(orders_df[orders_df['estado'] == "Pendiente"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Pedidos", total)
    col2.metric("Pendientes", pendientes)
    col3.metric("En Ruta", en_ruta)
    col4.metric("Entregados", entregados)
    
    st.subheader("Vista rápida de pedidos")
    st.dataframe(orders_df)

# --- ÓRDENES ---
elif choice == "Órdenes":
    st.title("📦 Órdenes Registradas")
    orders_df = get_orders()
    st.dataframe(orders_df)
    
# --- USUARIOS ---
elif choice == "Usuarios":
    st.title("👤 Usuarios Registrados")
    users_df = get_users()
    st.dataframe(users_df)
    
# --- AGREGAR PEDIDO ---
elif choice == "Agregar Pedido":
    st.title("➕ Agregar nuevo pedido")
    users_df = get_users()
    user_id = st.selectbox("Usuario", users_df["id"].tolist())
    origen = st.text_input("Origen")
    destino = st.text_input("Destino")
    estado = st.selectbox("Estado", ["Pendiente", "En ruta", "Entregado"])
    tiempo_estimado = st.number_input("Tiempo estimado (min)", min_value=1)
    hora_salida = st.time_input("Hora de salida", value=datetime.now().time())

    if st.button("Registrar Pedido"):
        # Combinar hora de salida con fecha actual para datetime completo
        salida_dt = datetime.combine(datetime.now().date(), hora_salida)
        insert_order(user_id, origen, destino, estado, tiempo_estimado, salida_dt)
        st.success("Pedido agregado correctamente")
        st.experimental_rerun()  # Recarga la app para ver cambios
