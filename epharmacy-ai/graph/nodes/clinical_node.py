def clinical_agent(state):
    docs = state.get("retrieved_docs", [])
    intent = state.get("intent", "GENERAL_INFO")

    rag_text = ""
    for i, doc in enumerate(docs, 1):
        rag_text += f"{i}. {doc['content']}\n"
        rag_text += f"   (Confidence: {doc['score']})\n\n"

    web_data = state.get("agent_outputs", {}).get("web")
    web_text = ""
    if web_data:
        web_text += web_data.get("content", "") + "\n"
        sources = web_data.get("sources", [])
        if sources:
            web_text += "\nSources:\n"
            for src in sources:
                web_text += f"- {src}\n"

    # ------------------------------
    # 🎯 Intent-based prioritization
    # ------------------------------
    if "latest" in state["user_query"].lower():
        # Web first, RAG as support
        response = "Latest safety information:\n\n"
        response += web_text
        response += "\n\nBackground information:\n"
        response += rag_text

    else:
        # Default: RAG first, Web as supplement
        response = "Based on verified medical sources:\n\n"
        response += rag_text
        if web_text:
            response += "\nAdditional information from web sources:\n"
            response += web_text

    state.setdefault("agent_outputs", {})
    state["agent_outputs"]["clinical"] = response
    return state
