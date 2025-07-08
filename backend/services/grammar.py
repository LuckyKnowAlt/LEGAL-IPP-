from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from pathlib import Path
import torch

router = APIRouter()

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "rugpt3large_based_on_gpt2"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if not MODEL_PATH.exists():
    raise RuntimeError(f"Grammar model not found in {MODEL_PATH}")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, local_files_only=True).to(DEVICE)

class GrammarRequest(BaseModel):
    text: str

class GrammarResponse(BaseModel):
    corrected: str

@router.post("/grammar", response_model=GrammarResponse)
def correct_grammar(req: GrammarRequest):
    input_text = "Исправь ошибки в следующем тексте:\n" + req.text.strip() + "\nИсправленный текст:"
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True).to(DEVICE)

    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95
    )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    corrected = decoded.split("Исправленный текст:")[-1].strip()
    return GrammarResponse(corrected=corrected)
