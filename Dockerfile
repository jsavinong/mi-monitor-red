# Dockerfile (versión para Docker Compose)

# Usamos una imagen base de Python
FROM python:3.11-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos primero el archivo de requerimientos
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el resto del código del proyecto
COPY . .