
# Utiliza una imagen base oficial de Python 3.8
FROM --platform=linux/amd64 python:3.10-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de dependencias al directorio actual
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de la aplicación al directorio de trabajo
COPY . .

# Hace que el puerto 5000 esté disponible para el mundo fuera de este contenedor
EXPOSE 5000

RUN python3 app.py

# Define el comando para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
