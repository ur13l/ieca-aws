# Descargar imagen base de python 3.11 desde Dockerhub
FROM --platform=linux/amd64 python:3.11-slim

# Utilizar directorio de trabajo
WORKDIR /app

# Copiar el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los demás archivos
COPY . .

# Exponer puerto de aplicación
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["flask", "run", "--host=0.0.0.0"] 