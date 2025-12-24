from vectorstore import load_vectorstore

db = load_vectorstore()

def retriever_node(state):
    docs = db.similarity_search(state["query"], k=4)
    contents = [doc.page_content for doc in docs]
    return {"documents": contents}
