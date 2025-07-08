from docx import Document
from nltk.tokenize import sent_tokenize
import nltk
nltk.download('punkt', quiet=True)

def load_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

def chunk_text(text: str, size: int = 500, overlap: int = 50) -> list[str]:
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
    # apply overlap
    out = []
    for i, c in enumerate(chunks):
        if i and overlap:
            prev = chunks[i-1]
            c = prev[-overlap:] + " " + c
        out.append(c)
    return out