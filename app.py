from flask import Flask, render_template, request
import sqlite3
import re
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def inicio():
    return "Laboratorio de Ciberseguridad"

# --- Funciones de Validación ---
def validar_usuario(usuario):
    # Entre 4 y 20 caracteres, solo letras, números y guion bajo
    return re.fullmatch(r"^[A-Za-z0-9_]{4,20}$", usuario) is not None

def validar_correo(correo):
    # Formato básico válido de correo
    return re.fullmatch(r"^[A-Za-z0-9.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", correo) is not None

def validar_password(password):
    # Mínimo 8 caracteres
    return len(password) >= 8

# --- Función de Registro de Eventos ---
def registrar_evento(tipo, usuario):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("eventos.log", "a", encoding="utf-8") as archivo:
        archivo.write(f"{fecha}, {tipo}, {usuario}\n")

# --- Ruta de Registro ---
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        # Saneamiento: strip() a usuario y correo (preservando la contraseña intacta)
        usuario = request.form.get("usuario", "").strip()
        correo = request.form.get("correo", "").strip()
        password = request.form.get("password", "")

        # Validaciones de seguridad
        if not validar_usuario(usuario):
            return "Usuario inválido"
        if not validar_correo(correo):
            return "Correo electrónico inválido"
        if not validar_password(password):
            return "La contraseña debe contener al menos 8 caracteres"

        conexion = sqlite3.connect("usuarios.db")
        cursor = conexion.cursor()

        # Comprobar duplicados con consulta parametrizada
        cursor.execute(
            "SELECT id FROM usuarios WHERE usuario = ? OR correo = ?",
            (usuario, correo)
        )
        existente = cursor.fetchone()

        if existente:
            conexion.close()
            return "El usuario o correo ya está registrado"

        # Aplicar hash seguro a la contraseña antes de guardar
        password_hash = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO usuarios (usuario, correo, password) VALUES (?, ?, ?)",
            (usuario, correo, password_hash)
        )
        conexion.commit()
        conexion.close()

        return "Usuario registrado"

    return render_template("registro.html")

# --- Ruta de Login ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "")

        conexion = sqlite3.connect("usuarios.db")
        cursor = conexion.cursor()

        # Consulta parametrizada buscando al usuario
        cursor.execute(
            "SELECT * FROM usuarios WHERE usuario = ?",
            (usuario,)
        )
        resultado = cursor.fetchone()
        conexion.close()

        # Verificar hash y registrar eventos
        if resultado and check_password_hash(resultado[3], password):
            registrar_evento("LOGIN_CORRECTO", usuario)
            return "Inicio de sesión correcto"
        else:
            registrar_evento("LOGIN_FALLIDO", usuario)
            return "Credenciales incorrectas"

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)