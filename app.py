# app.py
from flask import Flask, jsonify, render_template
import psycopg2 
from psycopg2.extras import RealDictCursor 
import os

# Creamos la aplicación web con Flask
app = Flask(__name__)

def obtener_conexion_db():
    """Función para conectarse a la base de datos."""
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    # --- IMPORTANTE ---
    # Le decimos a psycopg2 que nos devuelva los resultados como diccionarios.
    # La clave del diccionario será el nombre de la columna. ¡Súper conveniente!
    conn.cursor_factory = RealDictCursor
    return conn

# Definimos la RUTA principal de nuestra web (ej: www.misitio.com/)
@app.route('/')
def dashboard():
    """Esta función se ejecuta cuando alguien visita la página principal."""
    conn = obtener_conexion_db()
    cursor = conn.cursor()
    # Obtenemos los últimos 10 registros de salud para cada dispositivo
    # Esta es una consulta SQL un poco más avanzada
    query = """
    SELECT DISTINCT ON (hostname) *
    FROM device_health
    ORDER BY hostname, timestamp DESC;
    """
    cursor.execute(query)
    # El resultado de fetchall() ya es una lista de diccionarios!
    devices = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Le pasamos los datos a una plantilla HTML para que los muestre bonitos
    return render_template('dashboard.html', devices=devices)

# Esta es una ruta de API que devuelve los datos en formato JSON
# (Muy útil para que otras aplicaciones o Javascript lo consuman)
@app.route('/api/latest_status')
def api_latest_status():
    conn = obtener_conexion_db()
    cursor = conn.cursor()

    query = """
    SELECT DISTINCT ON (hostname) *
    FROM device_health
    ORDER BY hostname, timestamp DESC;
    """
    cursor.execute(query)
    devices = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(devices)


# Esto es para poder ejecutar la aplicación
if __name__ == '__main__':
    # debug=True hace que la web se reinicie sola cuando guardas cambios
    app.run(debug=True, port=5001)