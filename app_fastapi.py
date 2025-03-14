import os
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ✅ Configuración del modelo
MODEL_REPO = "fcp2207/Modelo_Phi2_fusionado"
HF_CACHE = "/tmp/huggingface_cache"
FEEDBACK_FILE = "/tmp/feedback.json"

os.environ["HF_HOME"] = HF_CACHE
os.makedirs(HF_CACHE, exist_ok=True)

# ✅ Inicializar FastAPI en puerto 7861
app = FastAPI(title="Phi-2 API", description="API optimizada con ajuste dinámico", version="1.6.2")

# ✅ Modelo de entrada
class InputData(BaseModel):
    input_text: str

# ✅ Cargar feedback
def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            return json.load(f)
    return {"temperature": 0.6, "top_p": 0.85, "top_k": 50, "repetition_penalty": 1.3}

def save_feedback(feedback):
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(feedback, f)

user_feedback = load_feedback()

# ✅ Cargar modelo
try:
    print("🔄 Cargando modelo desde Hugging Face...")
    model = AutoModelForCausalLM.from_pretrained(MODEL_REPO, torch_dtype="auto", device_map="auto", cache_dir=HF_CACHE)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_REPO, cache_dir=HF_CACHE)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        model.config.pad_token_id = tokenizer.eos_token_id

    print("✅ Modelo cargado correctamente.")
except Exception as e:
    print(f"❌ Error al cargar el modelo: {str(e)}")
    model, tokenizer = None, None

# ✅ Analizador de sentimiento
sentiment_analyzer = pipeline("sentiment-analysis")

@app.get("/")
def home():
    return {"message": "API con modelo fusionado ejecutándose 🚀"}

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
        raise HTTPException(status_code=500, detail=str(e))
