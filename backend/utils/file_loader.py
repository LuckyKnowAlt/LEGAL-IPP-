# file_loader.py
from docx import Document

def load_docx(path: str) -> str:
    """Загружает текст из .docx документа."""
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())