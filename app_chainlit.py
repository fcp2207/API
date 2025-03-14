import chainlit as cl
import requests
import os

# ✅ URL de la API en Hugging Face
HF_API_URL = "https://fcp2207-fusion-modelo-phi2-docker.hf.space/predict/"
HF_FEEDBACK_URL = "https://fcp2207-fusion-modelo-phi2-docker.hf.space/feedback/"  # 🔹 Nueva ruta para feedback

@cl.on_message
async def on_message(message: cl.Message):
    payload = {"input_text": message.content}
    
    try:
        response = requests.post(HF_API_URL, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json().get("response", "⚠️ Error: Respuesta no válida")
        
        # 🔹 Agregamos botones de feedback
        await cl.Message(
            content=result, 
            actions=[
                cl.Action(name="👍", label="Buena respuesta"),
                cl.Action(name="👎", label="Respuesta incorrecta")
            ]
        ).send()
        
    except requests.exceptions.RequestException as e:
        await cl.Message(content=f"❌ Error en la API: {str(e)}").send()

@cl.on_action("👍")
async def feedback_positive(action: cl.Action):
    """Envía feedback positivo a la API de Hugging Face."""
    requests.post(HF_FEEDBACK_URL, json={"feedback": "positivo"})
    await cl.Message(content="✅ ¡Gracias por tu feedback!").send()

@cl.on_action("👎")
async def feedback_negative(action: cl.Action):
    """Envía feedback negativo a la API de Hugging Face."""
    requests.post(HF_FEEDBACK_URL, json={"feedback": "negativo"})
    await cl.Message(content="⚠️ ¡Gracias! Ajustaremos el modelo.").send()




