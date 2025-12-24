from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def load_vectorstore():
    return FAISS.load_local(
        "pharmacy_db",
        HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        ),
        allow_dangerous_deserialization=True
    )
