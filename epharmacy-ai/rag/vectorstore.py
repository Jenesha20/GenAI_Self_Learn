from langchain_community.vectorstores import Chroma
from rag.embeddings import get_embedding_model

def create_vectorstore(docs, persist_dir="chroma_db"):
    embeddings = get_embedding_model()

    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_dir
    )

    vectordb.persist()
    return vectordb
