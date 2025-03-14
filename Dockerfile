FROM python:3.10

WORKDIR /app

COPY app_fastapi.py /app/app_fastapi.py
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7861

CMD ["uvicorn", "app_fastapi:app", "--host", "0.0.0.0", "--port", "7861"]

