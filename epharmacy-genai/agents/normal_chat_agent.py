from graph.state import GraphState
from tools.web_search_tool import web_search
from agents.llm_utils import call_llm
from agents.policies import MEDICAL_DISCLAIMER
import re

# Patterns that are too clinical → redirect elsewhere
STRICT_MEDICAL_PATTERNS = [
    r"dosage",
    r"how much",
    r"how often",
    r"interaction",
    r"safe to take",
    r"side effects",
]

# Patterns that are OK for normal chat (OTC level)
ALTERNATIVE_PATTERNS = [
    r"alternatives? for .*",
    r"substitutes? for .*",
    r"similar medicines to .*",
]

def normal_chat_node(state: GraphState) -> dict:
    query = state["messages"][-1]["content"]
    q_lower = query.lower()

    # -----------------------------
    # 1️⃣ Hard safety redirect
    # -----------------------------
    for p in STRICT_MEDICAL_PATTERNS:
        if re.search(p, q_lower):
            return {
                "final_answer": (
                    "That sounds like a medical decision. "
                    "It’s best to consult a doctor or pharmacist for safe guidance."
                )
            }

    # -----------------------------
    # 2️⃣ Special case: alternatives
    # -----------------------------
    is_alternative_query = any(re.search(p, q_lower) for p in ALTERNATIVE_PATTERNS)

    # -----------------------------
    # 3️⃣ Decide: chit-chat vs knowledge
    # -----------------------------
    is_small_talk = len(query.split()) <= 4 and not is_alternative_query

    context = ""
    if not is_small_talk:
        result = web_search(query)
        if result["status"] == "success":
            context = result["data"]["content"]

    # -----------------------------
    # 4️⃣ LLM rewrite with policy
    # -----------------------------
    memory_context = "\n".join(state.get("memory_notes", []))

    if is_alternative_query:
        instruction = """
You are a pharmacy assistant.
The user is asking about alternatives to a medicine.

Rules:
- Only suggest common OTC alternatives.
- Do NOT recommend prescription drugs.
- Be clear that these are general options, not medical advice.
- End with a suggestion to consult a pharmacist.
"""
    else:
        instruction = """
You are a friendly pharmacy assistant.

Rules:
- Answer conversationally and briefly.
- If information is unclear, say so.
- For medical uncertainty, advise consulting a doctor or pharmacist.
"""

    prompt = f"""
{instruction}

Session memory:
{memory_context}

User question:
{query}

Context (may be empty):
{context}
"""

    answer = call_llm(prompt)

    # add disclaimer for medical-ish answers
    if is_alternative_query:
        answer = answer + MEDICAL_DISCLAIMER

    return {
        "final_answer": answer
    }
