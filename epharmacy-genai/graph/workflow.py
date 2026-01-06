# from langgraph.graph import StateGraph, END
# from graph.state import GraphState, STATE_REDUCERS, is_blocked_by_safety

# # -----------------------------
# # IMPORT AGENT NODES
# # -----------------------------
# from agents.supervisor_agent import supervisor_node
# from agents.general_chat_agent import general_chat_node
# from agents.faq_agent import faq_node
# from agents.drug_interaction_agent import drug_interaction_node
# from agents.normal_chat_agent import normal_chat_node
# from agents.product_info_agent import product_info_node
# from agents.cart_management_agent import cart_management_node
# from agents.prescription_agent import prescription_node
# from agents.summarizer_agent import summarizer_node


# # -----------------------------
# # ROUTING FUNCTIONS
# # -----------------------------

# def route_from_supervisor(state: GraphState) -> str:
#     """
#     Supervisor can ONLY send to:
#     - general_chat
#     - product_info
#     """
#     intent = state.get("intent")

#     if intent == "general_chat":
#         return "general_chat"

#     if intent == "product_info":
#         return "product_info"

#     # everything else defaults safely
#     return "general_chat"


# def route_from_general_chat(state: GraphState) -> str:
#     sub = state.get("sub_intent")

#     if sub == "drug_interaction":
#         return "drug_interaction"
#     if sub == "faq":
#         return "faq"
#     return "normal_chat"


# def route_after_product_info(state: GraphState) -> str:
#     """
#     Cart is reachable ONLY after product info.
#     """
#     if state.get("cart_action") == "add":
#         return "cart_management"
#     return "summarizer"


# def route_after_cart(state: GraphState) -> str:
#     """
#     Prescription can happen ONLY after cart.
#     """
#     if state.get("requires_prescription"):
#         return "prescription"
#     return "summarizer"


# def route_after_prescription(state: GraphState) -> str:
#     return "summarizer"


# # -----------------------------
# # BUILD WORKFLOW
# # -----------------------------

# def build_workflow():

#     graph = StateGraph(GraphState, reducers=STATE_REDUCERS)

#     # -------------------------
#     # ADD NODES
#     # -------------------------
#     graph.add_node("supervisor", supervisor_node)
#     graph.add_node("general_chat", general_chat_node)
#     graph.add_node("faq", faq_node)
#     graph.add_node("drug_interaction", drug_interaction_node)
#     graph.add_node("normal_chat", normal_chat_node)
#     graph.add_node("product_info", product_info_node)
#     graph.add_node("cart_management", cart_management_node)
#     graph.add_node("prescription", prescription_node)
#     graph.add_node("summarizer", summarizer_node)

#     # -------------------------
#     # ENTRY POINT
#     # -------------------------
#     graph.set_entry_point("supervisor")

#     # -------------------------
#     # SUPERVISOR ROUTING
#     # -------------------------
#     graph.add_conditional_edges(
#         "supervisor",
#         route_from_supervisor,
#         {
#             "general_chat": "general_chat",
#             "product_info": "product_info",
#         },
#     )

#     # -------------------------
#     # GENERAL CHAT ROUTING
#     # -------------------------
#     graph.add_conditional_edges(
#         "general_chat",
#         route_from_general_chat,
#         {
#             "drug_interaction": "drug_interaction",
#             "faq": "faq",
#             "normal_chat": "normal_chat",
#         },
#     )

#     # chat leaves
#     graph.add_edge("faq", "summarizer")
#     graph.add_edge("drug_interaction", "summarizer")
#     graph.add_edge("normal_chat", "summarizer")

#     # -------------------------
#     # PRODUCT FLOW
#     # -------------------------
#     graph.add_conditional_edges(
#         "product_info",
#         route_after_product_info,
#         {
#             "cart_management": "cart_management",
#             "summarizer": "summarizer",
#         },
#     )

#     # -------------------------
#     # CART → PRESCRIPTION / SUMMARY
#     # -------------------------
#     graph.add_conditional_edges(
#         "cart_management",
#         route_after_cart,
#         {
#             "prescription": "prescription",
#             "summarizer": "summarizer",
#         },
#     )

#     # -------------------------
#     # PRESCRIPTION → SUMMARY
#     # -------------------------
#     graph.add_conditional_edges(
#         "prescription",
#         route_after_prescription,
#         {
#             "summarizer": "summarizer",
#         },
#     )

#     # -------------------------
#     # SAFETY OVERRIDE (GLOBAL)
#     # -------------------------
#     def safety_router(state: GraphState) -> str:
#         if is_blocked_by_safety(state):
#             return "summarizer"
#         return state.get("current_node")

#     # -------------------------
#     # EXIT
#     # -------------------------
#     graph.add_edge("summarizer", END)

#     # -------------------------
#     # COMPILE
#     # -------------------------
#     workflow = graph.compile()

#     png_bytes = workflow.get_graph().draw_mermaid_png()

#     with open("pharmacy_langgraph.png", "wb") as f:
#         f.write(png_bytes)

#     print("LangGraph visualization saved as pharmacy_langgraph.png")
#     return workflow



from langgraph.graph import StateGraph, END
from graph.state import GraphState, STATE_REDUCERS

from agents.supervisor_agent import supervisor_node
from agents.general_chat_agent import general_chat_node
from agents.faq_agent import faq_node
from agents.drug_interaction_agent import drug_interaction_node
from agents.normal_chat_agent import normal_chat_node
from agents.product_info_agent import product_info_node
from agents.cart_management_agent import cart_management_node
from agents.prescription_agent import prescription_node
from agents.summarizer_agent import summarizer_node


# ---------------- ROUTERS ----------------

def route_from_supervisor(state: GraphState):
    intent = state.get("intent")
    if intent == "product_info":
        return "product_info"
    return "general_chat"



def route_from_general_chat(state: GraphState):
    return state.get("sub_intent", "normal_chat")

def route_after_product(state: GraphState):
    if state.get("cart_action") == "add":
        return "cart_management"
    return "summarizer"

def route_after_cart(state: GraphState):
    if state.get("requires_prescription"):
        return "prescription"
    return "summarizer"


# ---------------- BUILD ----------------

def build_workflow():

    g = StateGraph(GraphState, reducers=STATE_REDUCERS)

    g.add_node("supervisor", supervisor_node)
    g.add_node("general_chat", general_chat_node)
    g.add_node("faq", faq_node)
    g.add_node("drug_interaction", drug_interaction_node)
    g.add_node("normal_chat", normal_chat_node)
    g.add_node("product_info", product_info_node)
    g.add_node("cart_management", cart_management_node)
    g.add_node("prescription", prescription_node)
    g.add_node("summarizer", summarizer_node)

    g.set_entry_point("supervisor")

    g.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {
            "general_chat": "general_chat",
            "product_info": "product_info",
        }
    )

    g.add_conditional_edges(
        "general_chat",
        route_from_general_chat,
        {
            "faq": "faq",
            "drug_interaction": "drug_interaction",
            "normal_chat": "normal_chat",
        }
    )

    g.add_edge("faq", "summarizer")
    g.add_edge("drug_interaction", "summarizer")
    g.add_edge("normal_chat", "summarizer")

    g.add_conditional_edges(
        "product_info",
        route_after_product,
        {
            "cart_management": "cart_management",
            "summarizer": "summarizer",
        }
    )

    g.add_conditional_edges(
        "cart_management",
        route_after_cart,
        {
            "prescription": "prescription",
            "summarizer": "summarizer",
        }
    )

    g.add_edge("prescription", "summarizer")
    g.add_edge("summarizer", END)

    workflow=g.compile()
    png_bytes = workflow.get_graph().draw_mermaid_png()

    with open("pharmacy_langgraph2.png", "wb") as f:
        f.write(png_bytes)

    print("LangGraph visualization saved as pharmacy_langgraph.png")
    # return workflow
    return g.compile()
