import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime
import pytz

# --- CONFIGURACIÓN DE CONEXIÓN ---
DATABASE_URL = "postgresql://postgres.aiiqkmslpfcleptmejfk:Brunokaliq12345@aws-0-us-east-2.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL)

# --- NOMBRES DE TABLAS Y COLUMNAS (ajusta si es necesario) ---
USERS_TABLE = "users"       # Cambia si tu tabla de usuarios tiene otro nombre
ORDERS_TABLE = "orders"     # Cambia si tu tabla de órdenes tiene otro nombre

# --- FUNCIONES AUXILIARES ---
@st.cache_data(ttl=600)
def get_users():
    try:
        query = f"SELECT * FROM {USERS_TABLE}"
        with engine.connect() as conn:
            return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"Error cargando usuarios: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=600)
def get_orders():
    try:
        query = f"SELECT * FROM {ORDERS_TABLE}"
        with engine.connect() as conn:
            return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"Error cargando órdenes: {e}")
        return pd.DataFrame()

def insert_order(user_id, origen, destino, estado, tiempo_estimado, hora_salida):
    try:
        insert_sql = text(f"""
            INSERT INTO {ORDERS_TABLE} (user_id, origen, destino, estado, tiempo_estimado_min, hora_salida)
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

# --- Inicializar variable en session_state para evitar inserciones dobles ---
if "pedido_agregado" not in st.session_state:
    st.session_state.pedido_agregado = False

# --- MENÚ LATERAL ---
st.sidebar.title("Menú")
menu = ["Dashboard", "Órdenes", "Usuarios", "Agregar Pedido"]
choice = st.sidebar.radio("Ir a:", menu)

# --- DASHBOARD ---
if choice == "Dashboard":
    st.title("📊 Dashboard de Logística")
    orders = get_orders()
    if not orders.empty:
        total = len(orders)
        # Ajusta los nombres de columna según tu tabla
        if 'estado' in orders.columns:
            en_ruta = len(orders[orders['estado'] == "En ruta"])
            entregados = len(orders[orders['estado'] == "Entregado"])
            pendientes = len(orders[orders['estado'] == "Pendiente"])
        else:
            en_ruta = entregados = pendientes = 0

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Pedidos", total)
        col2.metric("Pendientes", pendientes)
        col3.metric("En Ruta", en_ruta)
        col4.metric("Entregados", entregados)
        
        st.subheader("Vista rápida de pedidos")
        st.dataframe(orders)
    else:
        st.info("No hay datos de órdenes para mostrar.")

# --- ÓRDENES ---
elif choice == "Órdenes":
    st.title("📦 Órdenes Registradas")
    orders = get_orders()
    if not orders.empty:
        st.dataframe(orders)
    else:
        st.info("No hay órdenes registradas.")

# --- USUARIOS ---
elif choice == "Usuarios":
    st.title("👤 Usuarios Registrados")
    users = get_users()
    if not users.empty:
        st.dataframe(users)
    else:
        st.info("No hay usuarios registrados.")

# --- AGREGAR PEDIDO ---
elif choice == "Agregar Pedido":
    st.title("➕ Agregar nuevo pedido")
    users = get_users()
    if users.empty:
        st.warning("No hay usuarios disponibles para asignar el pedido.")
    else:
        user_id = st.selectbox("Usuario", users["id"].tolist())
        origen = st.text_input("Origen")
        destino = st.text_input("Destino")
        estado = st.selectbox("Estado", ["Pendiente", "En ruta", "Entregado"])
        tiempo_estimado = st.number_input("Tiempo estimado (min)", min_value=1)

        colombia_tz = pytz.timezone('America/Bogota')
        hora_actual_col = datetime.now(colombia_tz).time()
        hora_salida_raw = st.time_input("Hora de salida", value=hora_actual_col)
        hora_salida = datetime.combine(datetime.now(colombia_tz).date(), hora_salida_raw)

        if st.button("Registrar Pedido"):
            if not st.session_state.pedido_agregado:
                success, error = insert_order(user_id, origen, destino, estado, tiempo_estimado, hora_salida)
                if success:
                    st.success("Pedido agregado correctamente.")
                    st.session_state.pedido_agregado = True
                else:
                    st.error(f"Error al agregar pedido: {error}")
            else:
                st.warning("Ya has registrado un pedido. Para agregar otro, recarga la página.")

        if st.session_state.pedido_agregado:
            if st.button("Agregar otro pedido"):
                st.session_state.pedido_agregado = False
