import psycopg2  
import os 
import time
from datetime import datetime
import requests 

# La URL base de la API de nuestro dispositivo simulado
DEVICE_API_URL = "http://device-api:5002"

def recolectar_y_guardar():
    print(f"\n--- Iniciando ciclo de recolección: {datetime.now()} ---")
    
    conn = None 
    try:
        print("INFO: Conectando a la base de datos PostgreSQL...")
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),       
            dbname=os.getenv("DB_NAME"),     
            user=os.getenv("DB_USER"),       
            password=os.getenv("DB_PASSWORD")
        )
        cursor = conn.cursor()
        print("INFO: Conexión a PostgreSQL exitosa.")

        try:
            # La lógica de recolección de datos de la API
            print("INFO: Realizando petición a la API del dispositivo...")
            cpu_response = requests.get(f"{DEVICE_API_URL}/restconf/data/cisco-ios-xe-process-cpu-oper:cpu-usage")
            cpu_response.raise_for_status()
            cpu_data = cpu_response.json()
            
            cpu_usage = cpu_data["cisco-ios-xe-process-cpu-oper:cpu-usage"]["cpu-utilization"]["five-seconds-avg-util"]

            print(f"INFO: Uso de CPU actual: {cpu_usage}%")
            if cpu_usage > 80:
                print(f"ALERTA: ¡CPU alta detectada: {cpu_usage}%!")
            
            # Consulta SQL
            sql_query = """
            INSERT INTO device_health (hostname, cpu_usage, status, active_alarms)
            VALUES (%s, %s, %s, %s);
            """
            
            valores = ("Router-Principal", cpu_usage, "online", 0)
            
            cursor.execute(sql_query, valores)
            print("INFO: Datos de CPU de 'Router-Principal' guardados en la base de datos.")

        except requests.exceptions.RequestException as e:
            # La lógica de error de API
            print(f"ERROR: No se pudo conectar a la API del dispositivo. Error: {e}")
            sql_query = """
            INSERT INTO device_health (hostname, cpu_usage, status, active_alarms)
            VALUES (%s, %s, %s, %s);
            """
            # Usamos None para los valores que no tenemos
            valores = ("Router-Principal", None, "offline", "No disponible")
            cursor.execute(sql_query, valores)

        # Commit al final de todas las operaciones exitosas.
        conn.commit()

    except psycopg2.Error as e:
        # Manejo de errores específico para la conexión a la base de datos.
        print(f"ERROR: No se pudo conectar o escribir en la base de datos PostgreSQL. Error: {e}")

    finally:
        # <-- CAMBIO: Nos aseguramos de cerrar la conexión y el cursor si existen.
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
            print("INFO: Conexión a PostgreSQL cerrada.")

if __name__ == "__main__":
    # Esta parte es para esperar a que la BD esté lista al iniciar el contenedor.
    print("INFO: El servicio recolector ha iniciado. Esperando 15 segundos para que otros servicios arranquen...")
    time.sleep(15)
    while True:
        recolectar_y_guardar()
        print("--- Ciclo completado. Esperando 10 segundos... ---")
        time.sleep(10)