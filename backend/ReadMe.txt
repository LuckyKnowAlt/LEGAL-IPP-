# Legal Chatbot MVP - README

Этот проект представляет собой локальную RAG-систему (Retrieval-Augmented Generation) на FastAPI с поддержкой:

- Грамматической и юридической генерации (на базе ruGPT3)
- Перевода текстов (модель kazRush-ru-kk)
- Поиска по загруженным .docx-документам
- Простого веб-интерфейса на HTML + Tailwind + JS

===========================
🔧 СИСТЕМНЫЕ ТРЕБОВАНИЯ
===========================

- Python 3.10+
- Docker и Docker Compose (для контейнеризации)
- Git (если необходимо клонирование моделей)

===========================
⬇️ УСТАНОВКА И ПОДГОТОВКА
===========================

1. Убедитесь, что установлены `Docker` и `Docker Compose`.

2. Поместите свои `.docx` файлы в папку `documents/`.

3. Убедитесь, что у вас **две модели в папке `models/`**:


> ⚠️ Модели должны быть загружены из HuggingFace вручную или через скрипт.

===========================
🚀 ЗАПУСК ПРОЕКТА
===========================

ВНИМАНИЕ, Я ДОКЕР НЕ ИСПОЛЬЗОВАЛ. Т.Е. НЕ ТЕСТИЛ С НИМ.

В корне проекта выполните:
docker compose build
docker compose up

Сервисы будут доступны:
- API: http://localhost:8000
- Веб-интерфейс: http://localhost:8080

===========================
🧠 ЗАМЕНА МОДЕЛЕЙ
===========================

### Грамматическая модель (RAG)
- Путь задаётся в `main.py` и `rag.py`:
```python
      GENERATOR_MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "rugpt3large_based_on_gpt2"

Модель должна быть в формате AutoModelForCausalLM.

Переводческая модель
Путь задаётся в services/translate.py:
  MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "kazRush-ru-kk"

Используется T5Tokenizer и T5ForConditionalGeneration.

⚠️ При замене моделей — соблюдайте структуру и убедитесь, что все нужные файлы (config.json, tokenizer.json, model.safetensors и т.д.) присутствуют. А также, что используется соответствующий токенизатор.

===========================
📦 УСТАНОВКА БЕЗ DOCKER (альтернатива)

Если хотите запускать без контейнеров:

1. Установите зависимости:

bash
  cd backend
  pip install -r requirements.txt

2. Запустите FastAPI:

uvicorn main:app --reload

3. Откройте frontend/index.html в браузере.(Можно через VSCode пкм нажать на index.html и run with live server)

===========================
🌐 ИСПОЛЬЗОВАНИЕ
Загрузите документы в documents/.

Перезапустите сервер (docker-compose restart или uvicorn).

В браузере видите:

Вкладка "Grammar" — генерация юридического ответа.

Вкладка "Translate" — перевод текста.

Вкладка "QA & Template" — можно подключить дополнительные режимы.


===========================
❗ ПОЛЕЗНЫЕ КОМАНДЫ

Перезапустить:
  docker compose restart

Остановить:
  docker compose down

Очистить все контейнеры и образы:
  docker system prune -a


ЧТО ПО ХОРОШЕМУ НУЖНО СДЕЛАТЬ:
1. Использовать модель покруче.
2. Иметь хотя бы 1 документ в папке documents.
3. Сделать локальное сохранение истории переписок.
4. Продолжить тестировать разные параметры в RAG
5. Разделить логику на слои:

    Вынести модельную логику (AutoModel, generate, tokenize) в /models/ вместо смешивания с маршрутом (@router.post).

6. Улучшить работу с ChromaDB(Сделать отдельный сервис для инициализации коллекции, Кэшировать embeddings)

ЧТО МОЖНО СДЕЛАТЬ:
1. Создайте config.py:
   from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent
    MODELS_DIR = BASE_DIR.parent / "models"

    EMBED_MODEL_PATH = MODELS_DIR / "paraphrase-multilingual-MiniLM-L12-v2"
    GENERATOR_MODEL_PATH = MODELS_DIR / "rugpt3large_based_on_gpt2"
    TRANSLATE_MODEL_PATH = MODELS_DIR / "kazRush-ru-kk"

    CHROMA_DIR = BASE_DIR / "chroma_data"
    DOCS_DIR = BASE_DIR / "data" / "documents"
    
    Для использования в будущем:
    from app.config import GENERATOR_MODEL_PATH


ЗАМЕЧАНИЯ

Проект работает полностью оффлайн.

Весь функционал реализован через FastAPI REST endpoints.

Для UI используется Tailwind CSS + JS.
