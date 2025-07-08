# text_splitter.py
from nltk.tokenize import sent_tokenize
import nltk

nltk.download('punkt', quiet=True)

def chunk_text(text: str, size: int = 500, overlap: int = 50) -> list[str]:
    """Разбивает текст на чанки заданного размера с перекрытием."""
    sentences = sent_tokenize(text)
    chunks, cur = [], ""
    for sent in sentences:
        if len(cur) + len(sent) <= size:
            cur += " " + sent
        else:
            chunks.append(cur.strip())
            cur = sent
    if cur:
        chunks.append(cur.strip())
    # Применяем overlap
    out = []
    for i, c in enumerate(chunks):
        if i and overlap:
            prev = chunks[i-1]
            c = prev[-overlap:] + " " + c
        out.append(c)
    return out
