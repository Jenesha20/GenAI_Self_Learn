# from graph.state import GraphState

# def general_chat_node(state: GraphState) -> GraphState:
#     query = state.get("user_query", "").lower()

#     if any(k in query for k in ["together", "interaction", "mix"]):
#         state["sub_intent"] = "drug_interaction"
#     elif any(k in query for k in ["how", "what", "when", "where"]):
#         state["sub_intent"] = "faq"
#     else:
#         state["sub_intent"] = "normal_chat"

#     state["current_node"] = "general_chat"
#     return state


from graph.state import GraphState
from agents.semantic_router import SemanticRouter
from agents.router_examples import INTENT_EXAMPLES
import re

SUB_INTENT_EXAMPLES = {
    "drug_interaction": INTENT_EXAMPLES["drug_interaction"],
    "faq": INTENT_EXAMPLES["faq"],
    "normal_chat": INTENT_EXAMPLES["general_chat"],
}

router = SemanticRouter(SUB_INTENT_EXAMPLES)

LOW_CONF_THRESHOLD = 0.55
HIGH_CONF_THRESHOLD = 0.75

GREETING_PATTERNS = [
    r"^hi$", r"^hello$", r"^hey$", r"^hii$", r"^thanks$", r"^thank you$"
]

INTERACTION_PATTERNS = [
    r"take .* with .*",
    r"mix .* and .*",
    r"together",
    r"combine .*",
]


def general_chat_node(state: GraphState) -> dict:
    text = state["messages"][-1]["content"].lower().strip()

    # ------------------------------------------------
    # 1️⃣ HIGH-PRECISION OVERRIDES
    # ------------------------------------------------
    for p in GREETING_PATTERNS:
        if re.match(p, text):
            return {"sub_intent": "normal_chat"}

    for p in INTERACTION_PATTERNS:
        if re.search(p, text):
            return {"sub_intent": "drug_interaction"}

    # ------------------------------------------------
    # 2️⃣ SEMANTIC ROUTING (REUSED)
    # ------------------------------------------------
    label, score, scores = router.route(text)

    # ------------------------------------------------
    # 3️⃣ CONFIDENCE LOGIC
    # ------------------------------------------------
    if score >= HIGH_CONF_THRESHOLD:
        return {"sub_intent": label}

    if score >= LOW_CONF_THRESHOLD:
        return {"sub_intent": label}

    # ------------------------------------------------
    # 4️⃣ FALLBACK
    # ------------------------------------------------
    return {"sub_intent": "normal_chat"}
