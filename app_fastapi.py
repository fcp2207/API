import os
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ✅ Configuración de variables y modelo
MODEL_REPO = "fcp2207/Modelo_Phi2_fusionado"  # Asegúrate de que este es el correcto
HF_CACHE = "/tmp/huggingface_cache"
FEEDBACK_FILE = "/tmp/feedback.json"

# ✅ Configurar caché en Railway
os.environ["HF_HOME"] = HF_CACHE
os.makedirs(HF_CACHE, exist_ok=True)

# ✅ Inicializar FastAPI
app = FastAPI(title="Phi-2 API", description="API optimizada en Railway", version="2.0.1")

# ✅ Modelo de entrada
class InputData(BaseModel):
    input_text: str

# ✅ Cargar feedback si existe
def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            return json.load(f)
    return {"temperature": 0.6, "top_p": 0.85, "top_k": 50, "repetition_penalty": 1.3}

def save_feedback(feedback):
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(feedback, f)

user_feedback = load_feedback()

# ✅ Cargar modelo con optimización de memoria
try:
    print("🔄 Descargando y cargando el modelo en Railway...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_REPO, 
        torch_dtype=torch.float16, 
        device_map="auto", 
        cache_dir=HF_CACHE
    )
    tokenizer = AutoTokenizer.from_pretrained(MODEL_REPO, cache_dir=HF_CACHE)

    # ✅ Asegurar que haya un token de padding
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        model.config.pad_token_id = tokenizer.eos_token_id

    print("✅ Modelo cargado correctamente en Railway.")
except Exception as e:
    print(f"❌ Error al cargar el modelo en Railway: {str(e)}")
    model, tokenizer = None, None

# ✅ Analizador de sentimiento (Opcional)
sentiment_analyzer = pipeline("sentiment-analysis")

@app.get("/")
def home():
    return {"message": "API con modelo fusionado ejecutándose en Railway 🚀"}

@app.post("/predict/")
async def predict(data: InputData):
    if model is None or tokenizer is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado correctamente.")

    try:
        input_text = f"Responde en español: {data.input_text.strip()}"
        inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=512)

        with torch.no_grad():
            outputs = model.generate(
                **inputs, 
                max_new_tokens=200, 
                temperature=0.7, 
                top_p=0.9, 
                do_sample=True
            )

        return {"response": tokenizer.decode(outputs[0], skip_special_tokens=True)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de inferencia: {str(e)}")
