from graph.state import GraphState
from rag.retriever import retrieve_context

def faq_node(state: GraphState) -> GraphState:
    query = state["messages"][-1]["content"]
    chunks = retrieve_context(query)

    if not chunks:
        return {
            "is_safety_refusal": True
        }

    return {
        "faq_result": "\n".join(chunks)
    }
