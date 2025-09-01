# dispositivos_simulados.py

# Para simular que los datos cambian, importamos la librería 'random'
import random

def obtener_datos_dispositivo(hostname):
    """
    Esta función simula la conexión a un dispositivo de red y devuelve su estado.
    En un caso real, aquí iría el código para conectarse por SSH o API.
    """
    print(f"DEBUG: Conectando al dispositivo simulado '{hostname}'...")

    # Simulamos dos posibles dispositivos
    if hostname == "router-principal-sd":
        # Simulamos que a veces la CPU está alta
        cpu_usage = random.choice([25, 30, 85, 92])
        status = "online"
        alarms = random.choice([0, 1, 5])
        
    elif hostname == "switch-core-sti":
        # Simulamos que a veces este switch se cae
        status = random.choice(["online", "online", "online", "offline"])
        cpu_usage = random.choice([15, 20, 22])
        alarms = 0

    else:
        # Si el dispositivo no existe en nuestra simulación
        return None

    # Devolvemos los datos en un formato llamado "diccionario" (clave: valor)
    return {
        "hostname": hostname,
        "cpu_usage": cpu_usage,
        "status": status,
        "active_alarms": alarms
    }

# Ejemplo de cómo se usaría (puedes ignorar esto por ahora)
if __name__ == "__main__":
    datos_router = obtener_datos_dispositivo("router-principal-sd")
    print("Datos obtenidos:")
    print(datos_router)