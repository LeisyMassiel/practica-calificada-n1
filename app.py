from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__, template_folder='templates')

# Configuración de PostgreSQL en Render
DB_HOST = 'dpg-da7fkcs9v7es73bihf5g-a.virginia-postgres.render.com'
DB_NAME = 'test_db_im2w'
DB_USER = 'test_db_im2w_user'
DB_PASSWORD = 'GlvQHvpGflHcgjUuugeHSlV8FV6o0Y2S'
DB_PORT = '5432'

def conectar_db():
    try:
        return psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, sslmode='require')
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None

def crear_persona(dni, nombre, apellido, direccion, telefono):
    conn = conectar_db()
    if conn is None:
        return False
    cursor = conn.cursor()
    cursor.execute("INSERT INTO personas (dni, nombre, apellido, direccion, telefono) VALUES (%s, %s, %s, %s, %s)", (dni, nombre, apellido, direccion, telefono))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def obtener_registros():
    conn = conectar_db()
    if conn is None:
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas ORDER BY apellido")
    registros = cursor.fetchall()
    cursor.close()
    conn.close()
    return registros

def obtener_persona(id):
    conn = conectar_db()
    if conn is None:
        return None
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas WHERE id = %s", (id,))
    persona = cursor.fetchone()
    cursor.close()
    conn.close()
    return persona

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    dni = request.form['dni']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    crear_persona(dni, nombre, apellido, direccion, telefono)
    return redirect(url_for('administrar'))

@app.route('/administrar')
def administrar():
    registros = obtener_registros()
    return render_template('administrar.html', registros=registros)

@app.route('/editar/<int:id>')
def editar_registro(id):
    persona = obtener_persona(id)
    return render_template('editar.html', persona=persona)

@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar_registro(id):
    dni = request.form['dni']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    direccion = request.form['direccion']
    telefono = request.form['telefono']

    conn = conectar_db()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("UPDATE personas SET dni=%s, nombre=%s, apellido=%s, direccion=%s, telefono=%s WHERE id=%s", (dni, nombre, apellido, direccion, telefono, id))
        conn.commit()
        cursor.close()
        conn.close()

    return redirect(url_for('administrar'))

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_registro(id):
    conn = conectar_db()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM personas WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('administrar'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    
    
