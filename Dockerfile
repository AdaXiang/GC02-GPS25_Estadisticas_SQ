# Usamos Python ligero
FROM python:3.11-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Instalamos dependencias (Asegúrate de tener requirements.txt)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos TODO tu código (incluida la carpeta backend)
COPY . .

# Exponemos el puerto
EXPOSE 8000

# AQUÍ ESTÁ EL TRUCO:
# Ejecutamos uvicorn directamente, apuntando a backend.controller.fastapi:app
# y forzando el host 0.0.0.0
CMD ["uvicorn", "backend.controller.fastapi:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]