from flask import Flask, request, jsonify, render_template, redirect
import sqlite3
import os

app = Flask(__name__)

# Crear la base de datos y la tabla si no existen
def init_db():
    if not os.path.exists('database.db'):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                contrasena TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

# Ruta para registrar un nuevo usuario (API)
@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    usuario = data.get('usuario')
    contrasena = data.get('contrasena')

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)", (usuario, contrasena))
        conn.commit()
        return jsonify({"mensaje": "Registro exitoso"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 400
    finally:
        conn.close()

# Ruta para iniciar sesión (API)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('usuario')
    contrasena = data.get('contrasena')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND contrasena = ?", (usuario, contrasena))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"mensaje": "Autenticación satisfactoria"})
    else:
        return jsonify({"error": "Error en la autenticación"}), 401

# ==========================
# INTERFAZ WEB CON HTML
# ==========================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reciclafacil')
def reciclafacil():
    return render_template('ReciclaFácil.html')

@app.route('/registro_form')
def registro_form():
    return render_template('registro.html')

@app.route('/login_form')
def login_form():
    return render_template('login.html')

@app.route('/registro_web', methods=['POST'])
def registro_web():
    usuario = request.form.get('usuario')
    contrasena = request.form.get('contrasena')
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)", (usuario, contrasena))
        conn.commit()
        return redirect('/')
    except sqlite3.IntegrityError:
        return "El usuario ya existe", 400
    finally:
        conn.close()

@app.route('/login_web', methods=['POST'])
def login_web():
    usuario = request.form.get('usuario')
    contrasena = request.form.get('contrasena')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND contrasena = ?", (usuario, contrasena))
    user = cursor.fetchone()
    conn.close()
    if user:
        return f"¡Bienvenido, {usuario}!"
    else:
        return "Error en la autenticación", 401

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
