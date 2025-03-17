import chainlit as cl
import requests
import os

# ✅ URL de la API en Hugging Face
HF_API_URL = "https://fcp2207-fusion-modelo-phi2-docker.hf.space/predict/"
HF_FEEDBACK_URL = "https://fcp2207-fusion-modelo-phi2-docker.hf.space/feedback/"

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

        # 🔹 Actualiza el mensaje con la respuesta real
        await msg.update(content=result)

        # ✅ Manejo de feedback con `actions=` en lugar de `choices=`
        feedback_msg = await cl.Message(
            content="¿Cómo fue la respuesta?",
            actions=[
                cl.Action(name="👍", label="Buena respuesta", value={"feedback": "positivo", "response": result}),
                cl.Action(name="👎", label="Respuesta incorrecta", value={"feedback": "negativo", "response": result})
            ]
        ).send()

    except requests.exceptions.RequestException as e:
        print(f"❌ Error en la API: {e}")
        await msg.update(content=f"❌ Error en la API: {e}")

@cl.on_action("👍")
async def handle_positive_feedback(action: cl.Action):
    """Envía feedback positivo a la API."""
    requests.post(HF_FEEDBACK_URL, json=action.value)
    await cl.Message(content="✅ ¡Gracias por tu feedback! Seguiremos mejorando.").send()

@cl.on_action("👎")
async def handle_negative_feedback(action: cl.Action):
    """Envía feedback negativo a la API."""
    requests.post(HF_FEEDBACK_URL, json=action.value)
    await cl.Message(content="⚠️ ¡Gracias! Ajustaremos el modelo para mejorar las respuestas.").send()




