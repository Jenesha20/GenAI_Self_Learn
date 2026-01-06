from typing import List, Dict
from rag.embeddings import embed_texts
from rag.vectorstore import query_collection

def retrieve_context(query: str, top_k: int = 3) -> List[str]:
    query_vec = embed_texts([query])[0]
    results = query_collection(query_vec, top_k=top_k)

    docs = results.get("documents", [[]])[0]
    return docs
