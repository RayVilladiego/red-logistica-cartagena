import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE CONEXIÓN ---
DATABASE_URL = "postgresql://postgres.aiiqkmslpfcleptmejfk:Brunokaliq12345@aws-0-us-east-2.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL)

# --- FUNCIONES AUXILIARES ---
@st.cache_data
def get_users():
    return pd.read_sql("SELECT * FROM users", engine)

@st.cache_data
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
        # --- VERIFICACIÓN: contar registros después de insertar ---
        result = conn.execute(text("SELECT COUNT(*) FROM orders"))
        count = result.scalar()
        st.info(f"Registros actuales en orders: {count}")

# --- MENÚ LATERAL ---
st.sidebar.title("Menú")
menu = ["Dashboard", "Órdenes", "Usuarios", "Agregar Pedido"]
choice = st.sidebar.radio("Ir a:", menu)

# --- AGREGAR PEDIDO (PRUEBA) ---
if choice == "Agregar Pedido":
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

            # --- CONSULTA DIRECTA SIN CACHÉ ---
            with engine.connect() as conn:
                df_real = pd.read_sql("SELECT * FROM orders", conn)
            st.subheader("Pedidos directamente desde la BD (sin cache):")
            st.dataframe(df_real)
        except Exception as e:
            st.error(f"Error al agregar pedido: {e}")

# --- DASHBOARD ---
elif choice == "Dashboard":
    st.title("📊 Dashboard de Logística")
    orders = get_orders()
    st.dataframe(orders)

# --- ÓRDENES ---
elif choice == "Órdenes":
    st.title("📦 Órdenes Registradas")
    orders = get_orders()
    st.dataframe(orders)

# --- USUARIOS ---
elif choice == "Usuarios":
    st.title("👤 Usuarios Registrados")
    users = get_users()
    st.dataframe(users)
