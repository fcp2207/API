import chainlit as cl
import requests
import os

# ✅ URL de la API en Hugging Face
HF_API_URL = "https://fcp2207-fusion-modelo-phi2-docker.hf.space/predict/"

@cl.on_message
async def on_message(message):
    """ Maneja los mensajes en Chainlit y llama a la API. """

    # 🔹 Asegurar compatibilidad con versiones de Chainlit
    user_message = message.content if isinstance(message, cl.Message) else message  

    payload = {"input_text": user_message}

    try:
        num_tokens = len(user_message.split())
        timeout_value = min(120, 10 + (num_tokens * 2))

        # 🔹 Muestra mensaje de espera
        msg = cl.Message(content="⏳ Generando respuesta con GPU, por favor espera...")
        await msg.send()  

        # 🔹 Llamamos a la API y mostramos logs
        print(f"📡 Enviando solicitud a la API con timeout={timeout_value} segundos...")
        response = requests.post(HF_API_URL, json=payload, timeout=timeout_value)
        response.raise_for_status()  
        result = response.json().get("response", ⚠️ Error: Respuesta no válida")

        # 🔹 Mostrar logs en consola
        print(f"✅ Respuesta recibida: {result}")

        # 🔹 Actualiza el mensaje con la respuesta real
        msg.content = result  
        await msg.update()  

    except requests.exceptions.RequestException as e:
        print(f"❌ Error en la API: {e}")
        msg.content = f"❌ Error en la API: {e}"
        await msg.update()



