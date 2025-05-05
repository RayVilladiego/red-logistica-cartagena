# auth.py

import json
import os

USERS_FILE = "data/users.json"

def cargar_usuarios():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def guardar_usuarios(usuarios):
    with open(USERS_FILE, "w") as f:
        json.dump(usuarios, f, indent=4)

def autenticar_usuario(username, password):
    usuarios = cargar_usuarios()
    if username in usuarios and usuarios[username]["password"] == password:
        return True
    return False

def registrar_usuario(username, password, nombre_completo):
    usuarios = cargar_usuarios()
    if username not in usuarios:
        usuarios[username] = {
            "password": password,
            "nombre": nombre_completo
        }
        guardar_usuarios(usuarios)
        return True
    return False
