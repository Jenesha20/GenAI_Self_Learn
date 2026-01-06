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

# -----------------------------
# CONFIG
# -----------------------------
SAFETY_KEYWORDS = ["suicide", "kill myself", "overdose", "emergency"]
LOW_CONFIDENCE_THRESHOLD = 0.55
HIGH_CONFIDENCE_THRESHOLD = 0.75

router = SemanticRouter()


def supervisor_node(state: GraphState) -> dict:
    query = state["messages"][-1]["content"].lower()

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
    # 2️⃣ SEMANTIC ROUTING (primary)
    # ------------------------------------------------
    intent, score, all_scores = router.route(query)

    # ------------------------------------------------
    # 3️⃣ CONFIDENCE LOGIC
    # ------------------------------------------------
    # High confidence → trust router
    if score >= HIGH_CONFIDENCE_THRESHOLD:
        return {
            "intent": intent,
            "routing_confidence": score,
        }

    # Medium confidence → allow but cautious
    if score >= LOW_CONFIDENCE_THRESHOLD:
        return {
            "intent": intent,
            "routing_confidence": score,
        }

    # ------------------------------------------------
    # 4️⃣ FALLBACK / GUARDRAIL
    # ------------------------------------------------
    return {
        "intent": "general_chat",
        "routing_confidence": score,
        "needs_clarification": True,
    }
