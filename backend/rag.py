from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from pathlib import Path
from langdetect import detect

MODEL_PATH = Path(__file__).resolve().parent / "models" / "rugpt3large_based_on_gpt2"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if not MODEL_PATH.exists():
    raise RuntimeError(f"Generation model not found: {MODEL_PATH}")

# ✅ Строго указываем путь и отключаем fast-токенизатор
tokenizer = AutoTokenizer.from_pretrained(str(MODEL_PATH), local_files_only=True, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(str(MODEL_PATH), local_files_only=True).to(DEVICE)

def generate_answer(question: str, contexts: list[str], lang: str = "ru") -> str:
    try:
        # ✅ Правильная инициализация многострочной строки
        intro_ru = (
            "Ты — юридический помощник. Ответь на вопрос на основе следующей информации из документов. "
            "Пожалуйста, ответь развёрнуто, строго по делу, используя приведённые контексты.\n\n"
        )
        intro_kz = (
            "Сен — заң бойынша көмек көрсететін көмекші. "
            "Құжаттардағы ақпаратқа сүйене отырып, сұраққа жауап бер:\n\n"
        )

        prompt = intro_kz if lang == "kk" else intro_ru

        for i, ctx in enumerate(contexts, 1):
            prompt += f"[Контекст {i}]: {ctx.strip()}\n\n"
        prompt += f"[Вопрос]: {question.strip()}\n\n[Ответ]:"

        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024).to(DEVICE)

        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
        )

        decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # ✅ Возвращаем только текст после "[Ответ]:"
        if "[Ответ]:" in decoded:
            answer = decoded.split("[Ответ]:", 1)[-1].strip()
        else:
            answer = decoded.strip()

        return answer

    except Exception as e:
        return f"[Ошибка генерации: {str(e)}]"
