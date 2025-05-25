import streamlit as st
import base64
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime
from predict import predict_view
from dashboard_inteligente import show_dashboard

# --- FUNCIÓN DE FONDO CON OVERLAY OSCURO ---
def set_background(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: 
                linear-gradient(rgba(10, 18, 40, 0.68), rgba(10, 18, 40, 0.68)), 
                url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

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
    set_background("fondo_login.png")  # Fondo solo en login
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
else:
    set_background("fondo_panel.png")  # Fondo para toda la app luego del login

# --- MENÚ LATERAL ---
st.sidebar.title("Menú")
menu = [
    "Dashboard",
    "Órdenes",
    "Usuarios",
    "Agregar Pedido",
    "Panel Inteligente",  # <--- NUEVO: Panel Inteligente va aquí
    "Predicción",
    "Cerrar sesión"
]
choice = st.sidebar.radio("Ir a:", menu)

# --- RUTEO PRINCIPAL ---
if choice == "Dashboard":
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
    st.dataframe(orders)

elif choice == "Usuarios":
    st.title("👤 Usuarios Registrados")
    users = get_users()
    st.dataframe(users)

elif choice == "Agregar Pedido":
    st.title("➕ Agregar nuevo pedido")
    users = get_users()
    user_id = st.selectbox("Usuario", users["id"].tolist())
    origen = st.selectbox("Origen", zonas)
    destino = st.selectbox("Destino", zonas)
    estado = st.selectbox("Estado", ["Pendiente", "En ruta", "Entregado"])
    tiempo_estimado = st.number_input("Tiempo estimado (min)", min_value=1)
    hora_salida = st.time_input("Hora de salida", value=datetime.now().time())

    if st.button("Registrar Pedido"):
        hora_salida_dt = datetime.combine(datetime.now().date(), hora_salida)
        try:
            insert_order(user_id, origen, destino, estado, tiempo_estimado, hora_salida_dt)
            st.success("Pedido agregado correctamente")
            orders = get_orders()
            st.subheader("Vista rápida de pedidos")
            st.info(f"Total de pedidos en orders: {len(orders)}")
            st.dataframe(orders)
        except Exception as e:
            st.error(f"Error al agregar pedido: {e}")

elif choice == "Panel Inteligente":
    st.title("📈 Panel Inteligente de Logística")
    show_dashboard()

elif choice == "Predicción":
    st.title("🔮 Predicción de entrega")
    predict_view()

elif choice == "Cerrar sesión":
    st.session_state["logueado"] = False
    st.success("Sesión cerrada")
