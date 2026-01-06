from graph.state import GraphState
from rag.retriever import retrieve_context
from agents.llm_utils import call_llm
from agents.policies import MEDICAL_DISCLAIMER

# Example risk mapping (adapt to your KB)
def map_risk(chunks: list[str]) -> str:
    text = " ".join(chunks).lower()
    if "contraindicated" in text:
        return "high"
    if "use with caution" in text:
        return "medium"
    if "no known interaction" in text:
        return "low"
    return "unknown"


def drug_interaction_node(state: GraphState) -> dict:
    query = state["messages"][-1]["content"]

    # -----------------------------
    # 1️⃣ Retrieve from DDI KB
    # -----------------------------
    chunks = retrieve_context(query)

    # -----------------------------
    # 2️⃣ No data → safe fallback
    # -----------------------------
    if not chunks:
        return {
            "final_answer": (
                "I couldn’t find reliable information about this combination. "
                "It’s best to consult your doctor or pharmacist before taking these medicines together."
            ),
            "risk_level": "unknown",
        }

    # -----------------------------
    # 3️⃣ Risk classification
    # -----------------------------
    risk = map_risk(chunks)

    # -----------------------------
    # 4️⃣ LLM summarization (NOT source of truth)
    # -----------------------------
    context = "\n".join(chunks)

    prompt = f"""
You are a pharmacy assistant explaining drug interactions to patients.

User question:
{query}

Verified interaction data:
{context}

Instructions:
- Use ONLY the data above.
- Explain clearly and simply.
- Do NOT add new medical facts.
- Always include a safety disclaimer.
"""

    answer = call_llm(prompt)

    return {
        "final_answer": answer + MEDICAL_DISCLAIMER,
        "risk_level": risk,
    }
