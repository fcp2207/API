import chainlit as cl
import requests
import os

# ✅ URL de la API en Hugging Face
HF_API_URL = "https://fcp2207-fusion-modelo-phi2-docker.hf.space/predict/"

@cl.on_message
async def on_message(message: cl.Message):
    payload = {"input_text": message.content}
    
    try:
        response = requests.post(HF_API_URL, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json().get("response", "⚠️ Error: Respuesta no válida")
        
        await cl.Message(content=result).send()
    except requests.exceptions.RequestException as e:
        await cl.Message(content=f"❌ Error en la API: {str(e)}").send()


