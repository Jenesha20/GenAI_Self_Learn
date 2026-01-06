from typing import List
from pathlib import Path
import chromadb

# -----------------------------
# FORCE DISK PERSISTENCE
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent
CHROMA_DIR = BASE_DIR / "chroma_store"
CHROMA_DIR.mkdir(exist_ok=True)

# 🔥 Use PersistentClient (not Client)
_client = chromadb.PersistentClient(path=str(CHROMA_DIR))

COLLECTION_NAME = "epharmacy_knowledge"
_collection = None


def get_collection():
    global _collection
    if _collection is None:
        _collection = _client.get_or_create_collection(COLLECTION_NAME)
    return _collection


def add_documents(texts: List[str], embeddings: List[List[float]]):
    col = get_collection()

    start = col.count()
    ids = [f"doc_{start+i}" for i in range(len(texts))]

    col.add(
        documents=texts,
        embeddings=embeddings,
        ids=ids
    )


def query_collection(query_embedding: List[float], top_k: int = 3):
    col = get_collection()
    return col.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
