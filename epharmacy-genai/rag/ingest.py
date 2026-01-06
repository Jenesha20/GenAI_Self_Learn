from rag.loader import load_sources
from rag.chunking import chunk_text
from rag.embeddings import embed_texts
from rag.vectorstore import add_documents

def run_ingestion():
    print("Starting RAG ingestion...")

    sources = load_sources()
    all_chunks = []

    for text in sources:
        chunks = chunk_text(text)
        all_chunks.extend(chunks)

    print(f"Total chunks: {len(all_chunks)}")

    embeddings = embed_texts(all_chunks)

    add_documents(all_chunks, embeddings)

    print("RAG ingestion completed.")


# 🔥 THIS IS REQUIRED
if __name__ == "__main__":
    run_ingestion()
