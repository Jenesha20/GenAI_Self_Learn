def hallucination_check(state) -> bool:
    # Safety refusals are NOT hallucinations
    if state.get("is_safety_refusal"):
        return False

    docs = state.get("retrieved_docs", [])
    answer = state.get("final_answer", "")

    if not docs:
        return True

    return not any(doc["content"][:50] in answer for doc in docs)
