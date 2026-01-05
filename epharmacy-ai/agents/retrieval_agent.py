from langchain_chroma import Chroma
from rag.embeddings import get_embedding_model
from rag.retriever import retrieve_documents
from agents.entity_extractor import extract_entities
from graph.state import GraphState

def retrieval_agent(state: GraphState) -> GraphState:
    query = state["user_query"].lower()
    intent = state.get("intent", "GENERAL_INFO")
    entities = extract_entities(query)

    vectordb = Chroma(
        persist_directory="chroma_db",
        embedding_function=get_embedding_model()
    )

    docs = retrieve_documents(vectordb, query, k=12)

    # ---- identify primary entity ----
    primary_entity = entities[0] if entities else None

    entity_docs = []
    for doc in docs:
        meta = doc["metadata"]

        # STRICT entity match
        if meta.get("drug") != primary_entity:
            continue

        # STRICT intent gating
        if intent == "GENERAL_INFO" and meta.get("type") != "drug_info":
            continue

        entity_docs.append(doc)

    # HARD STOP — no fallback to other drugs
    state["retrieved_docs"] = entity_docs[:2]
    return state
