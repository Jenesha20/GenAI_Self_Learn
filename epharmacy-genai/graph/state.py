# from typing import TypedDict, List, Dict, Optional
# import operator

# # -----------------------------
# # STATE SCHEMA
# # -----------------------------

# class GraphState(TypedDict, total=False):

#     # -----------------------------
#     # Conversation Domain
#     # -----------------------------
#     user_id: str
#     user_query: str
#     conversation_id: str

#     # -----------------------------
#     # Routing Domain
#     # -----------------------------
#     intent: Optional[str]                 # general_chat | product_info | cart_action | prescription_flow
#     sub_intent: Optional[str]             # drug_interaction | faq | normal_chat
#     current_node: Optional[str]
#     next_node: Optional[str]

#     # -----------------------------
#     # Knowledge Domain
#     # -----------------------------
#     faq_result: Optional[str]
#     drug_interaction_result: Optional[str]
#     rag_context: List[str]

#     # -----------------------------
#     # Product Domain
#     # -----------------------------
#     product_query: Optional[str]
#     product_data: Optional[Dict]

#     # -----------------------------
#     # Cart Domain
#     # -----------------------------
#     cart_action: Optional[str]            # add | remove | update | view | clear
#     cart_items: List[Dict]
#     quantity_confirmed: bool
#     requires_prescription: bool

#     # -----------------------------
#     # Prescription Domain
#     # -----------------------------
#     prescription_uploaded: bool
#     prescription_verified: bool
#     prescription_status: Optional[str]    # pending | approved | rejected

#     # -----------------------------
#     # Tool Domain
#     # -----------------------------
#     tool_outputs: Dict
#     last_tool_used: Optional[str]

#     # -----------------------------
#     # Safety Domain
#     # -----------------------------
#     risk_level: Optional[str]             # low | medium | high
#     safety_flags: List[str]
#     is_safety_refusal: bool

#     # -----------------------------
#     # Error Domain
#     # -----------------------------
#     error_type: Optional[str]
#     error_message: Optional[str]
#     retry_count: int

#     # -----------------------------
#     # Output Domain
#     # -----------------------------
#     final_answer: Optional[str]
#     confidence_score: Optional[float]

#     # -----------------------------
#     # Metadata
#     # -----------------------------
#     state_version: str
#     schema_version: str

# def get_default_state() -> GraphState:
#     return {
#         "rag_context": [],
#         "cart_items": [],
#         "tool_outputs": {},
#         "safety_flags": [],
#         "quantity_confirmed": False,
#         "requires_prescription": False,
#         "prescription_uploaded": False,
#         "prescription_verified": False,
#         "retry_count": 0,
#         "is_safety_refusal": False,
#         "risk_level": "low",
#         "state_version": "1.0",
#         "schema_version": "1.0"
#     }

# # -----------------------------
# # REDUCERS
# # -----------------------------

# STATE_REDUCERS = {
#     "safety_flags": operator.add,
#     "rag_context": operator.add,
#     "cart_items": operator.add,
#     "tool_outputs": lambda a, b: {**a, **b},
# }

# # -----------------------------
# # VALIDATION HELPERS
# # -----------------------------

# MANDATORY_FIELDS = [
#     "user_query",
#     "risk_level",
#     "is_safety_refusal",
# ]

# def validate_state(state: GraphState) -> None:
#     for field in MANDATORY_FIELDS:
#         if field not in state:
#             raise ValueError(f"Missing mandatory state field: {field}")

# def require_fields(state: GraphState, fields: List[str], node_name: str):
#     for field in fields:
#         if field not in state or state[field] is None:
#             raise ValueError(
#                 f"[{node_name}] Missing required field: {field}"
#             )

# def is_blocked_by_safety(state: GraphState) -> bool:
#     return state.get("is_safety_refusal", False) is True

# def set_error(
#     state: GraphState,
#     error_type: str,
#     error_message: str
# ) -> GraphState:
#     state["error_type"] = error_type
#     state["error_message"] = error_message
#     state["retry_count"] = state.get("retry_count", 0) + 1
#     return state


from typing import TypedDict, List, Dict, Optional
import operator

class Message(TypedDict):
    role: str   # "user" | "assistant"
    content: str


class GraphState(TypedDict, total=False):

    # --- CORE MEMORY ---
    user_id: str
    conversation_id: str
    messages: List[Message]

    # --- ROUTING ---
    intent: Optional[str]        # general_chat | product_info
    sub_intent: Optional[str]    # faq | drug_interaction | normal_chat

    # --- PRODUCT ---
    product_data: Optional[Dict]
    requires_prescription: bool

    # --- CART ---
    cart_action: Optional[str]   # add | view
    cart_items: List[Dict]

    # --- RESULTS ---
    faq_result: Optional[str]
    drug_interaction_result: Optional[str]

    # --- OUTPUT ---
    final_answer: Optional[str]

    # --- SAFETY ---
    risk_level: str
    is_safety_refusal: bool


def get_default_state() -> GraphState:
    return {
        "messages": [],
        "cart_items": [],
        "risk_level": "low",
        "is_safety_refusal": False,
        "requires_prescription": False,
    }


STATE_REDUCERS = {
    "messages": operator.add,
    "cart_items": operator.add,

    # overwrite semantics
    "intent": lambda _old, new: new,
    "sub_intent": lambda _old, new: new,
    "product_data": lambda _old, new: new,
    "final_answer": lambda _old, new: new,
}
