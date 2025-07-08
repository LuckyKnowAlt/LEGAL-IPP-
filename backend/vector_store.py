from chromadb import PersistentClient
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from pathlib import Path

class VectorStore:
    def __init__(self, persist_directory, collection_name, embed_model: str):
        model_path = Path(embed_model)
        if not model_path.exists():
            raise RuntimeError(f"Embedder model path does not exist: {embed_model}")

        embed_fn = SentenceTransformerEmbeddingFunction(model_name=embed_model)

        client = PersistentClient(path=persist_directory)
        self.collection = client.get_or_create_collection(
            name=collection_name,
            embedding_function=embed_fn
        )

    def add_documents(self, docs: list[str], batch_size: int = 5000):
        for i in range(0, len(docs), batch_size):
            batch = docs[i:i+batch_size]
            ids = [f"doc-{i+j}" for j in range(len(batch))]
            self.collection.add(documents=batch, ids=ids)

    def query(self, text: str, k=3):
        result = self.collection.query(query_texts=[text], n_results=k)
        return result['documents'][0]