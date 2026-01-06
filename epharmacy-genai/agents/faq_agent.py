from graph.state import GraphState
from rag.retriever import retrieve_context
from agents.llm_utils import call_llm

def faq_node(state: GraphState) -> dict:
    query = state["messages"][-1]["content"]
    chunks = retrieve_context(query)

    # -----------------------------
    # 1️⃣ No FAQ found → human fallback
    # -----------------------------
    if not chunks:
        return {
            "final_answer": (
                "I couldn’t find this in our FAQs. "
                "This might need help from our support team. "
                "Would you like me to guide you on how to contact them?"
            )
        }

    # -----------------------------
    # 2️⃣ LLM synthesis
    # -----------------------------
    context = "\n".join(chunks)

    prompt = f"""
You are an assistant answering from official pharmacy FAQs.

User question:
{query}

FAQ content:
{context}

Instructions:
- Answer only using the FAQ content above.
- Be concise and clear.
- If the answer is uncertain or incomplete, say so and suggest contacting support.
"""

    answer = call_llm(prompt)

    return {
        "final_answer": answer
    }
