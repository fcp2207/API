# ✅ Usa una imagen oficial de Python optimizada
FROM python:3.10

# ✅ Configurar el directorio de trabajo dentro del contenedor
WORKDIR /app

# ✅ Copiar archivos necesarios dentro del contenedor
COPY app_chainlit.py /app/app_chainlit.py
COPY requirements.txt /app/requirements.txt

# ✅ Instalar dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Exponer el puerto 7860 (para Chainlit en Railway)
EXPOSE 7860

# ✅ Ejecutar Chainlit en Railway
CMD chainlit run /app/app_chainlit.py --port 7860 --host 0.0.0.0


