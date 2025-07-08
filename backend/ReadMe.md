# 📚 Legal Chatbot MVP

🔎 **Локальная RAG-система** на FastAPI с поддержкой:

- Грамматической и юридической генерации (на основе ruGPT3)
- Перевода текста (модель kazRush-ru-kk)
- Поиска по .docx-документам
- Простого веб-интерфейса на HTML + Tailwind + JS

---

## 🔧 Системные требования

- Python 3.10+
- Docker + Docker Compose (опционально)
- Git (если клонируете модели)

---

## 📁 Структура проекта

```
project-root/
├── backend/               # FastAPI сервер
│   ├── main.py            # Точка входа
│   ├── rag.py             # Генерация ответа (RAG)
│   ├── vector_store.py    # ChromaDB векторное хранилище
│   ├── utils/
│   │   ├── file_loader.py
│   │   └── text_splitter.py
│   ├── services/
│   │   ├── grammar.py
│   │   └── translate.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── models/
│   ├── rugpt3large_based_on_gpt2/
│   └── kazRush-ru-kk/
│
├── documents/             # Входные .docx документы
│   └── *.docx
│
├── frontend/              # UI
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── docker-compose.yml
```

---

## ⬇️ Установка и подготовка

1. Установите **Docker** и **Docker Compose**
2. Поместите `.docx` файлы в папку `documents/`
3. Поместите модели в `models/`:

```
models/
├── rugpt3large_based_on_gpt2/
│   ├── config.json
│   ├── model.safetensors
│   ├── tokenizer_config.json
│   └── vocab.json / merges.txt и пр.
└── kazRush-ru-kk/
    ├── config.json
    ├── spiece.model
    ├── tokenizer_config.json
    └── model.safetensors
```

> ⚠️ Модели нужно загрузить вручную с Hugging Face. Во время запуска интернет **не требуется**.
> Можно также через скрипт.

---

## 🚀 Запуск проекта

### Через Docker ВНИМАНИЕ, Я ДОКЕР НЕ ИСПОЛЬЗОВАЛ. Т.Е. НЕ ТЕСТИЛ С НИМ.
В корне проекта выполните:
```bash
docker compose build
docker compose up
```

Доступ:

- Backend API: [http://localhost:8000](http://localhost:8000)
- Frontend UI: [http://localhost:8080](http://localhost:8080)

### Без Docker (альтернатива)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Затем открой `frontend/index.html` в браузере (или через Live Server в VSCode).

---

## 🧠 Замена моделей

### Генерация (grammar, RAG)

```python
GENERATOR_MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "rugpt3large_based_on_gpt2"
```

> Модель должна быть совместима с `AutoModelForCausalLM`

### Перевод

```python
MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "kazRush-ru-kk"
```

> Используется `T5Tokenizer` и `T5ForConditionalGeneration`
⚠️ При замене моделей — соблюдайте структуру и убедитесь, что все нужные файлы (config.json, tokenizer.json, model.safetensors и т.д.) присутствуют. А также, что используется соответствующий токенизатор.
---

## 🌐 Использование

1. Загрузите документы в `documents/`
2. Перезапустите сервер
3. Откройте веб-интерфейс:
   - **Grammar** — генерация ответа
   - **Translate** — перевод
   - **QA & Template** — RAG

---

## ❗ Полезные команды

```bash
docker compose restart     # Перезапустить
docker compose down        # Остановить

docker system prune -a     # Очистка образов и контейнеров
```

---

## ✍️ Что по-хорошему нужно сделать

1. Использовать более мощную генеративную модель
2. Добавить хотя бы один docx-файл по умолчанию
3. Сохранять историю чатов локально (например, в JSON)
4. Настроить кеширование эмбеддингов
5. Разделить бизнес-логику и модельные вызовы в `/models/`
6. Вынести конфиги путей в отдельный `config.py`

Пример:

```python
# config.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR.parent / "models"

EMBED_MODEL_PATH = MODELS_DIR / "paraphrase-multilingual-MiniLM-L12-v2"
GENERATOR_MODEL_PATH = MODELS_DIR / "rugpt3large_based_on_gpt2"
TRANSLATE_MODEL_PATH = MODELS_DIR / "kazRush-ru-kk"

CHROMA_DIR = BASE_DIR / "chroma_data"
DOCS_DIR = BASE_DIR / "documents"
```



