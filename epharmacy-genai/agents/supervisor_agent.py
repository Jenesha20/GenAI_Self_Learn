# from graph.state import GraphState
# from agents.semantic_router import SemanticRouter
# from agents.llm_intent_classifier import llm_classify_intent
# import re

# SAFETY_KEYWORDS = ["suicide", "kill myself", "overdose", "emergency"]
# LOW_CONFIDENCE_THRESHOLD = 0.55
# HIGH_CONFIDENCE_THRESHOLD = 0.75

# ALTERNATIVE_PATTERNS = [
#     r"alternatives? for .*",
#     r"substitutes? for .*",
#     r"similar medicines to .*",
# ]

# CATEGORY_PATTERNS = [
#     r"products? for .*",
#     r"medicines? for .*",
#     r"what .* for .*",
# ]

# router = SemanticRouter()


# def supervisor_node(state: GraphState) -> dict:
#     query = state["messages"][-1]["content"].lower().strip()
#     ctx = state.get("context", {})

#     # ==================================================
#     # 0️⃣ 🔥 CONTEXT-FIRST OVERRIDES (MOST IMPORTANT)
#     # ==================================================
#     flow_state = state.get("flow_state")
#     if flow_state in ["awaiting_quantity", "awaiting_prescription"]:
#         return {"intent": "cart_action", "routing_confidence": 1.0}

#     if state.get("current_product"):
#         # Check if query is about this product
#         if any(word in query for word in ["add", "cart", "buy", "purchase"]):
#             return {"intent": "cart_action", "routing_confidence": 1.0}
#     # If user is responding to a cart / prescription flow
#     if ctx.get("pending_product") or ctx.get("last_product"):
#         if any(k in query for k in ["add", "remove", "yes", "no", "upload", "done"]):
#             return {"intent": "cart_action", "routing_confidence": 1.0}

#         # quantity-only reply
#         if query.isdigit():
#             return {"intent": "cart_action", "routing_confidence": 1.0}

#     # ==================================================
#     # 1️⃣ SAFETY GUARDRAIL
#     # ==================================================
#     if any(k in query for k in SAFETY_KEYWORDS):
#         return {
#             "intent": "general_chat",
#             "is_safety_refusal": True,
#             "risk_level": "high",
#         }

#     # ==================================================
#     # 2️⃣ HIGH-PRECISION OVERRIDES
#     # ==================================================
#     for p in ALTERNATIVE_PATTERNS:
#         if re.search(p, query):
#             return {"intent": "product_info", "routing_confidence": 1.0}

#     for p in CATEGORY_PATTERNS:
#         if re.search(p, query):
#             return {"intent": "product_info", "routing_confidence": 1.0}

#     # ==================================================
#     # 3️⃣ SEMANTIC ROUTING
#     # ==================================================
#     intent, score, all_scores = router.route(query)

#     if score >= HIGH_CONFIDENCE_THRESHOLD:
#         return {"intent": intent, "routing_confidence": score}

#     if score >= LOW_CONFIDENCE_THRESHOLD:
#         return {"intent": intent, "routing_confidence": score}

#     # ==================================================
#     # 4️⃣ 🔥 LLM FALLBACK
#     # ==================================================
#     llm_intent = llm_classify_intent(query)

#     return {
#         "intent": llm_intent,
#         "routing_confidence": score,
#         "used_llm_fallback": True,
#     }


from graph.state import GraphState
from agents.semantic_router import SemanticRouter
from agents.llm_intent_classifier import llm_classify_intent
import re

SAFETY_KEYWORDS = ["suicide", "kill myself", "overdose", "emergency"]
LOW_CONFIDENCE_THRESHOLD = 0.55
HIGH_CONFIDENCE_THRESHOLD = 0.75

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

# Cart-specific patterns
CART_PATTERNS = [
        r"add(?: to)? cart",
        r"buy (?:this|it|that)",
        r"purchase (?:this|it|that)",
        r"add (?:to|in) cart",
        r"put in cart",
        r"i(?:'ll| will)? take (?:it|this)",
    ]

router = SemanticRouter()


def supervisor_node(state: GraphState) -> dict:
    query = state["messages"][-1]["content"].lower().strip()
    ctx = state.get("context", {})
    
    print(f"🔍 SUPERVISOR: Processing query: '{query}'")
    
    # 🔥 Check if this is a response to quantity question
    if ctx.get("awaiting_quantity") and (query.isdigit() or "cancel" in query):
        print(f"✅ SUPERVISOR: Detected quantity response")
        return {"intent": "cart_action", "routing_confidence": 1.0}
    
    # Check for explicit cart actions
    CART_PATTERNS = [
        r"add(?: to)? cart",
        r"buy (?:this|it|that)",
        r"purchase (?:this|it|that)",
        r"add (?:to|in) cart",
        r"put in cart",
        r"add (?:it|this|that) (?:to|in) cart",
        r"i(?:'ll| will)? take (?:it|this)",
        r"i want (?:it|this)",
        r"get (?:it|this)",
    ]
    
    for pattern in CART_PATTERNS:
        if re.search(pattern, query):
            print(f"✅ SUPERVISOR: Detected cart action via pattern: {pattern}")
            return {"intent": "cart_action", "routing_confidence": 1.0}
    
    if ctx.get("awaiting_quantity") and (query.isdigit() or "cancel" in query):
        print(f"✅ SUPERVISOR: Detected quantity response -> cart_action")
        return {"intent": "cart_action", "routing_confidence": 1.0}
    
    # Also check state directly
    if state.get("awaiting_quantity") and (query.isdigit() or "cancel" in query):
        print(f"✅ SUPERVISOR: Detected quantity response (from state) -> cart_action")
        return {"intent": "cart_action", "routing_confidence": 1.0}
    
    # Check if previous context suggests cart action
    if ctx.get("last_product") or state.get("product_data"):
        cart_keywords = ["add", "buy", "purchase", "cart", "yes", "no", "quantity", "how many"]
        if any(keyword in query for keyword in cart_keywords):
            print(f"✅ SUPERVISOR: Detected cart intent from context + keywords")
            return {"intent": "cart_action", "routing_confidence": 1.0}
    
    # ... rest of your existing supervisor logic ...
    
    # Check flow state
    # if state.get("flow_state"):
    #     print(f"🔄 SUPERVISOR: Flow state detected: {state.get('flow_state')}")
    #     return {"intent": "cart_action", "routing_confidence": 1.0}

    # ==================================================
    # 1️⃣ SAFETY GUARDRAIL
    # ==================================================
    if any(k in query for k in SAFETY_KEYWORDS):
        return {
            "intent": "general_chat",
            "is_safety_refusal": True,
            "risk_level": "high",
        }

    # ==================================================
    # 2️⃣ HIGH-PRECISION OVERRIDES
    # ==================================================
    for p in ALTERNATIVE_PATTERNS:
        if re.search(p, query):
            return {"intent": "product_info", "routing_confidence": 1.0}

    for p in CATEGORY_PATTERNS:
        if re.search(p, query):
            return {"intent": "product_info", "routing_confidence": 1.0}

    # ==================================================
    # 3️⃣ SEMANTIC ROUTING
    # ==================================================
    intent, score, all_scores = router.route(query)
    
    print(f"🎯 SUPERVISOR: Semantic router intent: {intent}, score: {score}")

    if score >= HIGH_CONFIDENCE_THRESHOLD:
        return {"intent": intent, "routing_confidence": score}

    if score >= LOW_CONFIDENCE_THRESHOLD:
        return {"intent": intent, "routing_confidence": score}

    # ==================================================
    # 4️⃣ 🔥 LLM FALLBACK
    # ==================================================
    llm_intent = llm_classify_intent(query)
    print(f"🤖 SUPERVISOR: LLM fallback intent: {llm_intent}")

    return {
        "intent": llm_intent,
        "routing_confidence": score,
        "used_llm_fallback": True,
    }