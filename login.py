import streamlit as st
from auth import verify_password
from database import SessionLocal
from models import User

def login():
    st.title("Login")
    usuario = st.text_input("Usuario")
    clave = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        db = SessionLocal()
        user = db.query(User).filter(User.username == usuario).first()
        if user and verify_password(clave, user.hashed_password):
            st.session_state["logueado"] = True
            st.session_state["usuario"] = usuario
            st.success(f"Bienvenido {usuario}")
        else:
            st.error("Usuario o contraseña incorrectos")
