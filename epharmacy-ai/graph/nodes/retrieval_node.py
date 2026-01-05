from langchain_chroma import Chroma
from rag.embeddings import get_embedding_model
from rag.retriever import retrieve_documents

def retrieval_agent(state):
    query = state["user_query"]

    vectordb = Chroma(
        persist_directory="chroma_db",
        embedding_function=get_embedding_model()
    )

    docs = retrieve_documents(vectordb, query)

    state["retrieved_docs"] = docs
    return state
