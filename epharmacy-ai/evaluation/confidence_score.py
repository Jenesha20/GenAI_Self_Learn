def compute_confidence(retrieved_docs: list, risk_level: str) -> float:
    if not retrieved_docs:
        return 0.2

    avg_score = sum(d["score"] for d in retrieved_docs) / len(retrieved_docs)

    if risk_level == "HIGH":
        return min(avg_score, 0.6)

    return round(avg_score, 2)
