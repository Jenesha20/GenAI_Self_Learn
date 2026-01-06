from graph.state import GraphState
from tools.web_search_tool import web_search
from agents.llm_utils import call_llm
from agents.policies import MEDICAL_DISCLAIMER
import re

MEDICAL_PATTERNS = [
    r"take .*",
    r"dosage",
    r"side effects",
    r"interaction",
    r"safe to",
]

def normal_chat_node(state: GraphState) -> dict:
    query = state["messages"][-1]["content"]

    # -----------------------------
    # 1️⃣ SAFETY: medical queries should not be here
    # -----------------------------
    for p in MEDICAL_PATTERNS:
        if re.search(p, query.lower()):
            return {
                "final_answer": (
                    "It looks like you’re asking a medical question. "
                    "Let me route you to the right place to get safe information."
                )
            }

    # -----------------------------
    # 2️⃣ Decide: chit-chat or knowledge
    # -----------------------------
    is_small_talk = len(query.split()) <= 4

    context = ""
    if not is_small_talk:
        # use search for knowledge
        result = web_search(query)
        if result["status"] == "success":
            context = result["data"]["content"]

    # -----------------------------
    # 3️⃣ LLM rewrite
    # -----------------------------
    prompt = f"""
You are a friendly pharmacy assistant.

User question:
{query}

Search/context (may be empty):
{context}

Instructions:
- Answer conversationally and briefly.
- If information is unclear or conflicting, say you are not sure.
- For medical questions, advise consulting a doctor or pharmacist.
"""

    answer = call_llm(prompt)

    return {
        "final_answer": answer
    }
