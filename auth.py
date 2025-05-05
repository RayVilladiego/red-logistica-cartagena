# auth.py

import streamlit as st

def show_login():
    st.title("🔐 Iniciar Sesión")

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if username == "admin" and password == "1234":
            st.session_state["autenticado"] = True
            st.success("¡Ingreso exitoso!")
        else:
            st.error("Usuario o contraseña incorrectos")
