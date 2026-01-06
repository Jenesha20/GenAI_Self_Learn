from graph.state import GraphState
from rag.retriever import retrieve_context

def drug_interaction_node(state: GraphState) -> GraphState:
    query = state["messages"][-1]["content"]
    chunks = retrieve_context(query)

    if not chunks:
        return {
            "is_safety_refusal": True,
            "risk_level": "high"
        }

    return {
        "drug_interaction_result": "\n".join(chunks),
        "risk_level": "high"
    }
