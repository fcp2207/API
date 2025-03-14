# ✅ Usa una imagen oficial de Python optimizada
FROM python:3.10

# ✅ Configurar el directorio de trabajo dentro del contenedor
WORKDIR /app

# ✅ Copiar los archivos necesarios dentro del contenedor
COPY app_fastapi.py /app/app_fastapi.py
COPY requirements.txt /app/requirements.txt

# ✅ Instalar dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Crear directorios con permisos adecuados
RUN mkdir -p /tmp/huggingface_cache && chmod -R 777 /tmp

# ✅ Exponer el puerto 8080 (obligatorio en Railway)
EXPOSE 8080

# ✅ Ejecutar la API FastAPI en Railway
CMD uvicorn app_fastapi:app --host 0.0.0.0 --port 8080

