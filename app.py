import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime
from predict import predict_view
from auth import verify_password
import hashlib

# --- CONFIGURACIÓN DE CONEXIÓN ---
DATABASE_URL = "postgresql://postgres.aiiqkmslpfcleptmejfk:Brunokaliq12345@aws-0-us-east-2.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL)

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

# --- LOGIN ---
def login_block():
    st.title("🔒 Iniciar sesión")
    users = get_users()
    usernames = users["username"].tolist() if "username" in users else users["nombre"].tolist()
    username = st.selectbox("Usuario", usernames)
    password = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        user_row = users[users["username"] == username].iloc[0]
        if verify_password(password, user_row["hashed_password"]):
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

# --- MENÚ LATERAL ---
st.sidebar.title("Menú")
menu = ["Dashboard", "Órdenes", "Usuarios", "Agregar Pedido", "Predicción", "Cerrar sesión"]
choice = st.sidebar.radio("Ir a:", menu)

# --- CERRAR SESIÓN ---
if choice == "Cerrar sesión":
    st.session_state["logueado"] = False
    st.success("Sesión cerrada")
    st.experimental_rerun()

# --- DASHBOARD ---
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

# --- ÓRDENES ---
elif choice == "Órdenes":
    st.title("📦 Órdenes Registradas")
    orders = get_orders()
    st.info(f"Total de pedidos en orders: {len(orders)}")
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
        hora_salida_dt = datetime.combine(datetime.now().date(), hora_salida)
        try:
            insert_order(user_id, origen, destino, estado, tiempo_estimado, hora_salida_dt)
            st.success("Pedido agregado correctamente")
            # Mostrar pedidos recién insertados en la misma vista
            orders = get_orders()
            st.subheader("Vista rápida de pedidos")
            st.info(f"Total de pedidos en orders: {len(orders)}")
            st.dataframe(orders)
        except Exception as e:
            st.error(f"Error al agregar pedido: {e}")

# --- PREDICCIÓN (modelo ML/DL) ---
elif choice == "Predicción":
    st.title("🔮 Predicción de entrega")
    predict_view()  # Llama tu vista/modelo predictivo importado de predict.py

