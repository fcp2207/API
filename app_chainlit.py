import chainlit as cl
import requests
import os

# ✅ URL de la API en Hugging Face
HF_API_URL = "https://fcp2207-fusion-modelo-phi2-docker.hf.space/predict/"

@cl.on_message
async def on_message(message: cl.Message):
    payload = {"input_text": message.content}
    
    try:
        num_tokens = len(message.content.split())  
        timeout_value = min(120, 10 + (num_tokens * 2))  

        # 🔹 Muestra mensaje de espera dinámico
        msg = await cl.Message(content="⏳ Generando respuesta con GPU, por favor espera...").send()

        # 🔹 Llamamos a la API y mostramos logs
        print(f"📡 Enviando solicitud a la API con timeout={timeout_value} segundos...")
        response = requests.post(HF_API_URL, json=payload, timeout=timeout_value)
        response.raise_for_status()  # Captura cualquier error HTTP
        result = response.json().get("response", "⚠️ Error: Respuesta no válida")

        # 🔹 Mostrar logs en consola
        print(f"✅ Respuesta recibida: {result}")

        # 🔹 ACTUALIZACIÓN CORRECTA DEL MENSAJE EN CHAINLIT
        msg.content = result  # 🔹 Se actualiza el contenido del mensaje
        await msg.update()  # 🔹 Ahora se actualiza correctamente en Chainlit

    except requests.exceptions.RequestException as e:
        print(f"❌ Error en la API: {e}")
        msg.content = f"❌ Error en la API: {e}"
        await msg.update()




