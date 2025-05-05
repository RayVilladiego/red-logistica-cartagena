# auth.py

import streamlit as st

def show_login():
    st.title("🔐 Iniciar Sesión")

    with st.form("login_form"):
        usuario = st.text_input("Usuario")
        contraseña = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Iniciar Sesión")

        if submit:
            if usuario == "admin" and contraseña == "1234":
                st.session_state["autenticado"] = True
                st.success("Inicio de sesión exitoso ✅")
            else:
                st.error("Credenciales incorrectas. Intenta nuevamente ❌")
