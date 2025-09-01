# api_dispositivo_realista.py
from flask import Flask, jsonify
import random
import datetime

app = Flask(__name__)

# Datos base que simulan la configuración y estado de las interfaces
INTERFACES_DATA = {
    "ietf-interfaces:interfaces": {
        "interface": [
            {
                "name": "GigabitEthernet0/1",
                "description": "Uplink to Core-SW",
                "type": "iana-if-type:ethernetCsmacd",
                "enabled": True,
                "ietf-interfaces:statistics": {
                    "discontinuity-time": "2025-01-01T00:00:00Z",
                    "in-octets": 0,
                    "out-octets": 0
                }
            },
            {
                "name": "GigabitEthernet0/2",
                "description": "Connection to Server-Farm",
                "type": "iana-if-type:ethernetCsmacd",
                "enabled": True,
                "ietf-interfaces:statistics": {
                    "discontinuity-time": "2025-01-01T00:00:00Z",
                    "in-octets": 0,
                    "out-octets": 0
                }
            },
            {
                "name": "Loopback0",
                "description": "Management Interface",
                "type": "iana-if-type:softwareLoopback",
                "enabled": False,
                "ietf-interfaces:statistics": {
                    "discontinuity-time": "2025-01-01T00:00:00Z",
                    "in-octets": 0,
                    "out-octets": 0
                }
            }
        ]
    }
}

# Esta es la ruta que un recolector consultaría para obtener datos de interfaces
@app.route('/restconf/data/ietf-interfaces:interfaces')
def get_interfaces():
    # Simulamos que el tráfico cambia en cada petición
    for interface in INTERFACES_DATA["ietf-interfaces:interfaces"]["interface"]:
        if interface["enabled"]:
            # Aumentamos los contadores de forma realista
            interface["ietf-interfaces:statistics"]["in-octets"] += random.randint(10000, 500000)
            interface["ietf-interfaces:statistics"]["out-octets"] += random.randint(5000, 250000)

    return jsonify(INTERFACES_DATA)

# Esta es otra ruta común, para ver la salud del sistema
@app.route('/restconf/data/cisco-ios-xe-process-cpu-oper:cpu-usage')
def get_cpu_health():
    health_data = {
        "cisco-ios-xe-process-cpu-oper:cpu-usage": {
            "cpu-utilization": {
                "five-seconds-avg-util": random.choice([10, 12, 15, 40, 88]), # Simulamos picos de CPU
                "one-minute": random.randint(10, 25),
                "five-minutes": random.randint(10, 20)
            }
        }
    }
    return jsonify(health_data)

if __name__ == '__main__':
    # Corremos esta API en el puerto 5002 para no chocar con nuestra app de dashboard
    app.run(host='0.0.0.0', debug=True, port=5002)