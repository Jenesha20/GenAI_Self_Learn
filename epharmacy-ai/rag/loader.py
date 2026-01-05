from langchain_community.document_loaders import PyPDFLoader, TextLoader
import os

def load_documents(file_paths: list):
    docs = []

    for path in file_paths:
        ext = os.path.splitext(path)[1].lower()

        if ext == ".pdf":
            loader = PyPDFLoader(path)
            docs.extend(loader.load())

        elif ext == ".txt":
            loader = TextLoader(path, encoding="utf-8")
            docs.extend(loader.load())

        else:
            raise ValueError(f"Unsupported file type: {ext}")

    return docs
