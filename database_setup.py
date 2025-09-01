# database_setup.py
import psycopg2
import os # Para leer variables de entorno
import time

def setup_database():
    conn = None
    for i in range(5): # Intentar conectar 5 veces
        try:
            print("Intentando conectar a la base de datos PostgreSQL...")
            # Leemos los datos de conexión de variables de entorno (más seguro)
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD")
            )
            print("¡Conexión a PostgreSQL exitosa!")
            break # Salimos del bucle si la conexión es exitosa
        except psycopg2.OperationalError as e:
            print(f"Error de conexión: {e}. Reintentando en 5 segundos...")
            time.sleep(5)

    if conn is None:
        print("No se pudo conectar a la base de datos después de varios intentos. Abortando.")
        exit(1)

    cursor = conn.cursor()

    # La sintaxis de SQL es ligeramente diferente para PostgreSQL
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS device_health (
        id SERIAL PRIMARY KEY,
        hostname TEXT NOT NULL,
        cpu_usage INTEGER,
        status TEXT,
        active_alarms INTEGER,
        timestamp TIMESTAMPTZ DEFAULT NOW()
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Base de datos y tabla 'device_health' configuradas exitosamente.")

if __name__ == "__main__":
    setup_database()