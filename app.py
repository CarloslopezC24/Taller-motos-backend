import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql  # Conector para MariaDB / MySQL 

app = Flask(__name__)
CORS(app)  

# -------------------------------------------------------
# CONFIGURACIÓN DE CONEXIONES (Base de datos y Nube)
# -------------------------------------------------------
DB_HOST = os.environ.get('DB_HOST', 'mysql-carloshale26.alwaysdata.net')  
DB_USER = os.environ.get('DB_USER', 'carloshale26')
DB_PASS = os.environ.get('DB_PASS', 'Carlos2204')
DB_NAME = os.environ.get('DB_NAME', 'carloshale26_tallermotos')

# Configuración del Servicio de Correo SMTP (Gmail en la nube) 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_REMITENTE = "cabreracarlos1415@gmail.com"
EMAIL_PASSWORD = "caxy qzpa irug klav"

def obtener_conexion():
    """Establece una conexión limpia con la base de datos MariaDB."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/login', methods=['POST'])
def login():
    """Permite el inicio de sesión básico del usuario administrador."""
    data = request.get_json()
    
    if not data or 'usuario' not in data or 'password' not in data:
        return jsonify({"error": "Faltan campos obligatorios"}), 400
        
    usuario = data.get('usuario').strip()
    password = data.get('password').strip()
    
    if not usuario or not password:
        return jsonify({"error": "El usuario y la contraseña no pueden estar vacíos"}), 400

    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "SELECT id, usuario, email, rol FROM usuarios WHERE usuario = %s AND password = %s"
            cursor.execute(sql, (usuario, password))
            user_record = cursor.fetchone()
            
        conexion.close()
        
        if user_record:
            return jsonify({
                "mensaje": "Inicio de sesión exitoso",
                "usuario": user_record
            }), 200
        else:
            return jsonify({"error": "Credenciales inválidas"}), 401
            
    except Exception as e:
        print(f"Error en login: {e}")
        return jsonify({"error": "Error interno del servidor al consultar la sesión"}), 500

@app.route('/registros', methods=['GET'])
def listar_registros():
    """Obtiene todos los registros activos del taller de motos."""
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "SELECT id, nombre, categoria, descripcion, precio, destacado, activo FROM registros WHERE activo = 1"
            cursor.execute(sql)
            resultados = cursor.fetchall()
        conexion.close()
        
        return jsonify(resultados), 200  
    except Exception as e:
        print(f"Error al listar: {e}")
        return jsonify({"error": "No se pudieron cargar los registros"}), 500

@app.route('/registros', methods=['POST'])
def agregar_registro():
    """Inserta un nuevo servicio de mantenimiento o reparación en la base de datos."""
    data = request.get_json()
    
    if not data or 'nombre' not in data or 'categoria' not in data or 'precio' not in data:
        return jsonify({"error": "Datos incompletos. Nombre, categoría y precio son obligatorios"}), 400
        
    nombre = data.get('nombre').strip()
    categoria = data.get('categoria').strip()
    descripcion = data.get('descripcion', '').strip()
    precio = data.get('precio')
    destacado = data.get('destacado', 0)

    if not nombre or not categoria:
        return jsonify({"error": "El nombre y la categoría no pueden enviarse vacíos"}), 400
        
    try:
        precio_numerico = float(precio)
        if precio_numerico <= 0:
            return jsonify({"error": "El precio debe ser un número mayor a cero"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "El precio provisto debe ser un tipo de dato numérico válido"}), 400

    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = """INSERT INTO registros (nombre, categoria, descripcion, precio, activo, destacado) 
                     VALUES (%s, %s, %s, %s, 1, %s)"""
            cursor.execute(sql, (nombre, categoria, descripcion, precio_numerico, destacado))
            conexion.commit()
        conexion.close()
        
        return jsonify({"mensaje": "Registro del taller guardado correctamente en la base de datos"}), 201
    except Exception as e:
        print(f"Error al insertar: {e}")
        return jsonify({"error": "Error de persistencia al intentar guardar el servicio"}), 500

@app.route('/registros/desactivar/<int:id_registro>', methods=['POST'])
def desactivar_registro(id_registro):
    """Realiza una baja lógica (activo = 0) del servicio seleccionado."""
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "UPDATE registros SET activo = 0 WHERE id = %s"
            cursor.execute(sql, (id_registro,))
            conexion.commit()
        conexion.close()
        
        return jsonify({"mensaje": "El registro ha sido quitado del catálogo"}), 200
    except Exception as e:
        print(f"Error al desactivar: {e}")
        return jsonify({"error": "No se pudo actualizar el estado del registro"}), 500

@app.route('/enviar-alerta', methods=['POST'])
def enviar_alerta():
    """Dispara un correo de confirmación real utilizando el servidor en la nube de Google."""
    data = request.get_json()
    
    if not data or 'mensaje' not in data:
        return jsonify({"error": "Contenido del mensaje ausente"}), 400
        
    asunto = data.get('asunto', 'Notificación - Culiacán Bikers Garage')
    mensaje_texto = data.get('mensaje')
    destinatario = data.get('destinatario', 'cabreracarlos1415@gmail.com')

    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_REMITENTE
        msg['To'] = destinatario
        msg['Subject'] = asunto
        msg.attach(MIMEText(mensaje_texto, 'plain', 'utf-8'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  
        server.login(EMAIL_REMITENTE, EMAIL_PASSWORD)
        server.sendmail(EMAIL_REMITENTE, destinatario, msg.as_string())
        server.quit()

        return jsonify({"mensaje": "Servicio de correo en la nube ejecutado de manera exitosa"}), 200
    except Exception as e:
        print(f"Error en pasarela de correos: {e}")
        return jsonify({"error": "El servidor de correos rechazó la autenticación o conexión"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)