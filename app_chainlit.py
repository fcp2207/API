import chainlit as cl
import requests
import os

# ✅ URL de la API en Hugging Face
HF_API_URL = "https://fcp2207-fusion-modelo-phi2-docker.hf.space/predict/"
HF_FEEDBACK_URL = "https://fcp2207-fusion-modelo-phi2-docker.hf.space/feedback/"

@cl.on_message
async def on_message(message):
    """ Maneja los mensajes en Chainlit y llama a la API. """
    
    # 🔹 Asegurar compatibilidad con versiones de Chainlit
    user_message = message.content if isinstance(message, cl.Message) else message  # ✅ Compatibilidad para versiones nuevas y antiguas
    
    payload = {"input_text": user_message}

    try:
        num_tokens = len(user_message.split())
        timeout_value = min(120, 10 + (num_tokens * 2))

        # 🔹 Muestra mensaje de espera
        msg = cl.Message(content="⏳ Generando respuesta con GPU, por favor espera...")
        await msg.send()  # ✅ Enviar mensaje correctamente antes de actualizarlo

        # 🔹 Llamamos a la API y mostramos logs
        print(f"📡 Enviando solicitud a la API con timeout={timeout_value} segundos...")
        response = requests.post(HF_API_URL, json=payload, timeout=timeout_value)
        response.raise_for_status()  # Captura cualquier error HTTP
        result = response.json().get("response", "⚠️ Error: Respuesta no válida")

        # 🔹 Mostrar logs en consola
        print(f"✅ Respuesta recibida: {result}")

        # 🔹 Actualiza el mensaje con la respuesta real
        msg.content = result  # ✅ Se actualiza el contenido del mensaje
        await msg.update()  # ✅ Se usa `.update()` sin argumentos en Chainlit 0.7.0+

        # ✅ Manejo de feedback con `cl.AskUserMessage`
        feedback = await cl.AskUserMessage(
            content="¿Cómo fue la respuesta?",
            actions=[
                cl.Action(name="positivo", label="👍 Buena respuesta", value="positivo"),
                cl.Action(name="negativo", label="👎 Respuesta incorrecta", value="negativo")
            ]
        ).send()

        if feedback:
            feedback_data = {"feedback": feedback.value, "response": result}
            requests.post(HF_FEEDBACK_URL, json=feedback_data)

            # 🔹 Mostrar mensaje de confirmación
            await cl.Message(content="✅ ¡Gracias por tu feedback! Seguiremos mejorando.").send()

    except requests.exceptions.RequestException as e:
        print(f"❌ Error en la API: {e}")
        msg.content = f"❌ Error en la API: {e}"
        await msg.update()





