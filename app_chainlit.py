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
        response = requests.post(HF_API_URL, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json().get("response", "⚠️ Error: Respuesta no válida")
        
        # 🔹 Muestra la respuesta y agrega botones
        msg = await cl.Message(content=result).send()

        # ✅ Manejo de feedback con `@cl.step`
        feedback = await cl.AskUserMessage(
            content="¿Cómo fue la respuesta?",
            options=["👍 Buena respuesta", "👎 Respuesta incorrecta"]
        ).send()

        if feedback and feedback.content == "👍 Buena respuesta":
            requests.post(HF_FEEDBACK_URL, json={"feedback": "positivo"})
        elif feedback and feedback.content == "👎 Respuesta incorrecta":
            requests.post(HF_FEEDBACK_URL, json={"feedback": "negativo"})

    except requests.exceptions.RequestException as e:
        await cl.Message(content=f"❌ Error en la API: {str(e)}").send()




