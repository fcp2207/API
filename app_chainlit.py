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
        msg = await cl.Message(content="⏳ Generando respuesta, por favor espera...").send()
        
        response = requests.post(HF_API_URL, json=payload, timeout=timeout_value)
        response.raise_for_status()
        result = response.json().get("response", "⚠️ Error: Respuesta no válida")

        # 🔹 Actualiza el mensaje con la respuesta real
        msg.update(content=result)

        # ✅ Manejo de feedback con `AskUserMessage`
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



