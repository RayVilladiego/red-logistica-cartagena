import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime
import pytz

# --- Configuración de la conexión ---
DATABASE_URL = "postgresql://postgres.aiiqkmslpfcleptmejfk:Brunokaliq12345@aws-0-us-east-2.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL, future=True)

# --- Inicializar estados ---
if "pedido_agregado" not in st.session_state:
    st.session_state.pedido_agregado = False

# --- Funciones auxiliares ---
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

# --- Menú lateral ---
st.sidebar.title("Menú")
menu = ["Dashboard", "Órdenes", "Usuarios", "Agregar Pedido"]
choice = st.sidebar.radio("Ir a:", menu)

# --- Dashboard ---
if choice == "Dashboard":
    st.title("📊 Dashboard de Logística")
    orders = get_orders()
    if not orders.empty:
        total = len(orders)
        en_ruta = len(orders[orders['estado'] == "En ruta"]) if 'estado' in orders.columns else 0
        entregados = len(orders[orders['estado'] == "Entregado"]) if 'estado' in orders.columns else 0
        pendientes = len(orders[orders['estado'] == "Pendiente"]) if 'estado' in orders.columns else 0

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Pedidos", total)
        c2.metric("Pendientes", pendientes)
        c3.metric("En Ruta", en_ruta)
        c4.metric("Entregados", entregados)

        st.subheader("Vista rápida de pedidos")
        st.dataframe(orders)
    else:
        st.info("No hay datos de órdenes.")

# --- Órdenes ---
elif choice == "Órdenes":
    st.title("📦 Órdenes Registradas")
    orders = get_orders()
    if not orders.empty:
        st.dataframe(orders)
    else:
        st.info("No hay órdenes registradas.")

# --- Usuarios ---
elif choice == "Usuarios":
    st.title("👤 Usuarios Registrados")
    users = get_users()
    if not users.empty:
        st.dataframe(users)
    else:
        st.info("No hay usuarios registrados.")

# --- Agregar Pedido ---
elif choice == "Agregar Pedido":
    st.title("➕ Agregar nuevo pedido")
    users = get_users()
    if users.empty:
        st.warning("No hay usuarios disponibles para asignar.")
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

        if st.session_state.pedido_agregado:
            st.success("Pedido agregado correctamente.")
            if st.button("Agregar otro pedido"):
                st.session_state.pedido_agregado = False
        else:
            if st.button("Registrar Pedido"):
                success, error = insert_order(user_id, origen, destino, estado, tiempo_estimado, hora_salida)
                if success:
                    st.session_state.pedido_agregado = True
                    st.experimental_rerun()
                else:
                    st.error(f"Error al agregar pedido: {error}")
