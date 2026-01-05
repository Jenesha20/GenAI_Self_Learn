def clinical_agent(state):
    docs = state.get("retrieved_docs", [])

    response = "Based on verified medical sources:\n\n"
    for i, doc in enumerate(docs, 1):
        response += f"{i}. {doc['content']}\n"
        response += f"   (Confidence: {round(doc['score'], 2)})\n\n"

    state["agent_outputs"]["clinical"] = response
    return state
