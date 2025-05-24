import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime
from predict import predict_view
from about import show_about  # Importa el mensaje de bienvenida

# --- CONFIGURACIÓN DE CONEXIÓN ---
DATABASE_URL = "postgresql://postgres.aiiqkmslpfcleptmejfk:Brunokaliq12345@aws-0-us-east-2.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL)

# --- LISTA DE ZONAS DISPONIBLES ---
zonas = [
    "Mamonal", "Bocagrande", "Centro", "Getsemaní", "El Pozón", "San Felipe", "Crespo", "Pie de la Popa",
    "Manga", "Los Alpes", "La Boquilla", "El Bosque", "El Laguito", "Otro"
]

# --- FUNCIONES AUXILIARES ---
def get_users():
    return pd.read_sql("SELECT * FROM users", engine)

def get_orders():
    return pd.read_sql("SELECT * FROM orders", engine)

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

# --- LOGIN (FIJO: admin / 1234) ---
def login_block():
    st.title("🔒 Iniciar sesión")
    username = st.selectbox("Usuario", ["admin"])
    password = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if username == "admin" and password == "1234":
            st.session_state["logueado"] = True
            st.session_state["usuario"] = username
            st.success("¡Sesión iniciada correctamente!")
            st.experimental_rerun()
        else:
            st.error("Usuario o contraseña incorrectos")
    st.stop()

# --- CONTROL DE SESIÓN ---
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

if not st.session_state["logueado"]:
    login_block()

# --- MENÚ LATERAL: Incluye Presentación primero ---
st.sidebar.title("Menú")
menu = [
    "Presentación",
    "Dashboard",
    "Órdenes",
    "Usuarios",
    "Agregar Pedido",
    "Predicción",
    "Cerrar sesión"
]
choice = st.sidebar.radio("Ir a:", menu)

# --- RUTEO PRINCIPAL ---
if choice == "Presentación":
    show_about()

elif choice == "Dashboard":
    st.title("📊 Dashboard de Logística")
    orders = get_orders()
    st.info(f"Total de pedidos en orders: {len(orders)}")
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

elif choice == "Órdenes":
    st.title("📦 Órdenes Registradas")
    orders = get_orders()
    st.info(f"Total de pedidos en orders: {len(orders)}")
    s
