import streamlit as st

# Simulación de usuarios
USUARIOS = {
    "admin": "1234",
    "operador": "5678"
}

def login():
    st.title("Login de Usuario")
    usuario = st.text_input("Usuario")
    contraseña = st.text_input("Contraseña", type="password")
    if st.button("Iniciar sesión"):
        if usuario in USUARIOS and USUARIOS[usuario] == contraseña:
            st.success(f"Bienvenido, {usuario}!")
            st.session_state["autenticado"] = True
        else:
            st.error("Credenciales incorrectas")
