from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from pathlib import Path
import torch
import os
import traceback

router = APIRouter()

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "kazRush-ru-kk"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = None
model = None

try:
    print(f"[INFO] Загрузка модели перевода из: {MODEL_PATH}")
    print("[INFO] Файлы модели:", os.listdir(MODEL_PATH))

    tokenizer = AutoTokenizer.from_pretrained(str(MODEL_PATH), local_files_only=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(str(MODEL_PATH), local_files_only=True).to(DEVICE)

    print("[INFO] Модель и токенизатор успешно загружены")

except Exception as e:
    print("[ERROR] Ошибка загрузки модели перевода:")
    traceback.print_exc()
    tokenizer = None
    model = None

class TranslateRequest(BaseModel):
    text: str

class TranslateResponse(BaseModel):
    translated: str

@router.post("/translate", response_model=TranslateResponse)
def translate(req: TranslateRequest):
    if tokenizer is None or model is None:
        raise HTTPException(status_code=500, detail="Модель перевода не загружена")

    try:
        print(f"[DEBUG] Входной текст: {req.text}")
        inputs = tokenizer(req.text, return_tensors="pt").to(DEVICE)
        outputs = model.generate(inputs["input_ids"], max_new_tokens=512, num_beams=5)
        translated = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"[DEBUG] Переведённый текст: {translated}")
        return TranslateResponse(translated=translated)

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка генерации перевода: {e}")
