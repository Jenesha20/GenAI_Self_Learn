from rag.loader import load_documents
from rag.chunking import chunk_documents
from rag.vectorstore import create_vectorstore

pdfs = [
    "data/drug_labels.pdf",
    "data/drug_interactions.txt",
    "data/faq.txt"
]

docs = load_documents(pdfs)
chunks = chunk_documents(docs)
create_vectorstore(chunks)

print("✅ Chroma DB created successfully")
