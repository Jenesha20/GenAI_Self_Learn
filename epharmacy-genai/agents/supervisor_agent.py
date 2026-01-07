# from graph.state import GraphState

# def supervisor_node(state: GraphState) -> GraphState:
#     query = state.get("user_query", "").lower()

#     # -----------------------------
#     # COMMERCE FLOW (highest priority)
#     # -----------------------------
#     if any(k in query for k in ["add", "cart", "buy", "purchase"]):
#         state["intent"] = "product_info"
#         return state

#     # -----------------------------
#     # PRODUCT INFO FLOW
#     # -----------------------------
#     if any(k in query for k in ["product", "price", "cost", "info", "details"]):
#         state["intent"] = "product_info"
#         return state

#     # -----------------------------
#     # GENERAL CHAT
#     # -----------------------------
#     state["intent"] = "general_chat"
#     return state


from graph.state import GraphState
from agents.semantic_router import SemanticRouter
import re

# -----------------------------
# CONFIG
# -----------------------------
SAFETY_KEYWORDS = ["suicide", "kill myself", "overdose", "emergency"]
LOW_CONFIDENCE_THRESHOLD = 0.55
HIGH_CONFIDENCE_THRESHOLD = 0.75

# 🔥 High-precision intent overrides
ALTERNATIVE_PATTERNS = [
    r"alternatives? for .*",
    r"substitutes? for .*",
    r"similar medicines to .*",
]

CATEGORY_PATTERNS = [
    r"products? for .*",
    r"medicines? for .*",
    r"what .* for .*",
]

router = SemanticRouter()


def supervisor_node(state: GraphState) -> dict:
    query = state["messages"][-1]["content"].lower().strip()

    # ------------------------------------------------
    # 1️⃣ SAFETY GUARDRAIL (hard rules)
    # ------------------------------------------------
    if any(k in query for k in SAFETY_KEYWORDS):
        return {
            "intent": "general_chat",
            "is_safety_refusal": True,
            "risk_level": "high",
        }

    # ------------------------------------------------
    # 2️⃣ HIGH-PRECISION OVERRIDES
    # ------------------------------------------------

    # Alternatives → normal/general chat (NOT product flow)
    for p in ALTERNATIVE_PATTERNS:
        if re.search(p, query):
            return {
                "intent": "general_chat",
                "routing_confidence": 1.0,
            }

    # Category browsing → product info
    for p in CATEGORY_PATTERNS:
        if re.search(p, query):
            return {
                "intent": "product_info",
                "routing_confidence": 1.0,
            }

    # ------------------------------------------------
    # 3️⃣ SEMANTIC ROUTING (primary)
    # ------------------------------------------------
    intent, score, all_scores = router.route(query)

    # ------------------------------------------------
    # 4️⃣ CONFIDENCE LOGIC
    # ------------------------------------------------
    if score >= HIGH_CONFIDENCE_THRESHOLD:
        return {
            "intent": intent,
            "routing_confidence": score,
        }

    if score >= LOW_CONFIDENCE_THRESHOLD:
        return {
            "intent": intent,
            "routing_confidence": score,
        }

    # ------------------------------------------------
    # 5️⃣ FALLBACK
    # ------------------------------------------------
    return {
        "intent": "general_chat",
        "routing_confidence": score,
        "needs_clarification": True,
    }
