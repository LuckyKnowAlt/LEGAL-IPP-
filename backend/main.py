from pathlib import Path
import os
import chromadb
from services import grammar, translate
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.file_loader import load_docx
from utils.text_splitter import chunk_text
from vector_store import VectorStore
from rag import generate_answer
from langdetect import detect

app = FastAPI(title="Legal Chatbot RAG Only")

app.include_router(grammar.router)
app.include_router(translate.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

EMBED_MODEL_PATH = Path(__file__).resolve().parent / "models" / "paraphrase-multilingual-MiniLM-L12-v2"
GENERATOR_MODEL_PATH = Path(__file__).resolve().parent / "models" / "rugpt3large_based_on_gpt2"

if not EMBED_MODEL_PATH.exists():
    raise RuntimeError(f"Embedder model not found: {EMBED_MODEL_PATH}")
if not GENERATOR_MODEL_PATH.exists():
    raise RuntimeError(f"Generator model not found: {GENERATOR_MODEL_PATH}")

vs = VectorStore(
    persist_directory="chroma_data",
    collection_name="legal_docs",
    embed_model=str(EMBED_MODEL_PATH)
)

docs_dir = "documents"
all_chunks = []
if os.path.isdir(docs_dir):
    for fname in os.listdir(docs_dir):
        if fname.lower().endswith(".docx"):
            path = os.path.join(docs_dir, fname)
            text = load_docx(path)
            chunks = chunk_text(text)
            all_chunks.extend(chunks)

if not all_chunks:
    raise RuntimeError(f"No .docx files found in `{docs_dir}`")

vs.add_documents(all_chunks)

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    generated: str

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    q = req.question.strip()
    if not q:
        raise HTTPException(400, "Empty question")

    lang = detect(q)
    lang = "kk" if lang == "kk" else "ru"

    contexts = vs.query(q, k=1)
    generated = generate_answer(q, contexts, lang=lang)
    return AskResponse(generated=generated)
