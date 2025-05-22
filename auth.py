import streamlit as st

# Usuarios de ejemplo — en producción usa base de datos segura
USUARIOS = {
    "admin": "1234",
    "usuario": "pass"
}

def login():
    st.sidebar.title("🔒 Login")
    usuario = st.sidebar.text_input("Usuario")
    clave = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Ingresar"):
        if usuario in USUARIOS and USUARIOS[usuario] == clave:
            st.session_state['login'] = True
            st.session_state['usuario'] = usuario
            st.sidebar.success(f"Bienvenido, {usuario}!")
        else:
            st.sidebar.error("Usuario o contraseña incorrectos")
    return st.session_state.get('login', False)

# En tu app principal:
# if login():
#    ... contenido protegido ...
# else:
#    st.warning("Por favor inicia sesión para continuar")
