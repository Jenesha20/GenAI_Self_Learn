from agents.llm_utils import call_llm
import json

ALLOWED_INTENTS = [
    "product_info",
    "cart_action",
    "drug_interaction",
    "faq",
    "general_chat",
]

def llm_classify_intent(query: str) -> str:
    prompt = f"""
You are an intent classifier for an e-pharmacy chatbot.

Classify the user's intent into ONE of:
{", ".join(ALLOWED_INTENTS)}

User message:
"{query}"

Return JSON only:
{{ "intent": "<one_of_the_allowed_intents>" }}
"""

    try:
        resp = call_llm(prompt)
        data = json.loads(resp)
        intent = data.get("intent")

        if intent in ALLOWED_INTENTS:
            return intent
    except Exception:
        pass

    return "general_chat"
