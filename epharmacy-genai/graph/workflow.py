# from langgraph.graph import StateGraph, END
# from graph.state import GraphState, STATE_REDUCERS

# from agents.supervisor_agent import supervisor_node
# from agents.general_chat_agent import general_chat_node
# from agents.faq_agent import faq_node
# from agents.drug_interaction_agent import drug_interaction_node
# from agents.normal_chat_agent import normal_chat_node
# from agents.product_info_agent import product_info_node
# from agents.cart_management_agent import cart_management_node
# from agents.prescription_agent import prescription_node
# from agents.summarizer_agent import summarizer_node


# # ---------------- ROUTERS ----------------

# def route_from_supervisor(state: GraphState):
#     intent = state.get("intent")

#     if intent == "product_info":
#         return "product_info"

#     if intent == "cart_action":
#         return "cart_management"

#     return "general_chat"



# def route_from_general_chat(state: GraphState):
#     return state.get("sub_intent", "normal_chat")

# def route_after_product(state: GraphState):
#     if state.get("cart_action") == "add":
#         return "cart_management"
#     return "summarizer"

# def route_after_cart(state: GraphState):
#     """Better routing after cart operations"""
    
#     # If prescription is required and not yet verified
#     if state.get("requires_prescription") and state.get("prescription_status") != "verified":
#         return "prescription"
    
#     # If we're still in quantity selection flow
#     if state.get("flow_state") == "awaiting_quantity":
#         return "cart_management"
    
#     # Otherwise summarize
#     return "summarizer"

# def route_after_prescription(state: GraphState):
#     """Route after prescription verification"""
    
#     # If prescription is now verified, go back to cart to ask for quantity
#     if state.get("prescription_status") == "verified":
#         return "cart_management"
    
#     # If rejected, go to summarizer
#     return "summarizer"



# # ---------------- BUILD ----------------

# def build_workflow():

#     g = StateGraph(GraphState, reducers=STATE_REDUCERS)

#     g.add_node("supervisor", supervisor_node)
#     g.add_node("general_chat", general_chat_node)
#     g.add_node("faq", faq_node)
#     g.add_node("drug_interaction", drug_interaction_node)
#     g.add_node("normal_chat", normal_chat_node)
#     g.add_node("product_info", product_info_node)
#     g.add_node("cart_management", cart_management_node)
#     g.add_node("prescription", prescription_node)
#     g.add_node("summarizer", summarizer_node)

#     g.set_entry_point("supervisor")

#     g.add_conditional_edges(
#         "supervisor",
#         route_from_supervisor,
#         {
#             "general_chat": "general_chat",
#             "product_info": "product_info",
#             "cart_management": "cart_management",
#         }
#     )

#     g.add_conditional_edges(
#         "general_chat",
#         route_from_general_chat,
#         {
#             "faq": "faq",
#             "drug_interaction": "drug_interaction",
#             "normal_chat": "normal_chat",
#         }
#     )

#     g.add_edge("faq", "summarizer")
#     g.add_edge("drug_interaction", "summarizer")
#     g.add_edge("normal_chat", "summarizer")

#     g.add_conditional_edges(
#         "product_info",
#         route_after_product,
#         {
#             "cart_management": "cart_management",
#             "summarizer": "summarizer",
#         }
#     )

#     g.add_conditional_edges(
#         "cart_management",
#         route_after_cart,
#         {
#             "prescription": "prescription",
#             "summarizer": "summarizer",
#         }
#     )
#     g.add_conditional_edges(
#     "prescription",
#     route_after_prescription,
#     {
#         "cart_management": "cart_management",
#         "summarizer": "summarizer",
#     }
# )

#     g.add_edge("prescription", "summarizer")
#     g.add_edge("summarizer", END)

#     workflow=g.compile()
#     png_bytes = workflow.get_graph().draw_mermaid_png()

#     with open("pharmacy_langgraph2.png", "wb") as f:
#         f.write(png_bytes)

#     print("LangGraph visualization saved as pharmacy_langgraph.png")
#     # return workflow
#     return g.compile()



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
    user_msg = state["messages"][-1]["content"].lower() if state.get("messages") else ""
    
    print(f"🔄 ROUTER: Supervisor intent: {intent}")
    print(f"🔄 ROUTER: User message: {user_msg}")
    
    # 🔥 CRITICAL: If user is responding to a quantity question
    if state.get("awaiting_quantity") and (user_msg.strip().isdigit() or "cancel" in user_msg):
        print(f"🔄 ROUTER: Quantity response detected -> cart_management")
        return "cart_management"
    
    # Normal routing
    if intent == "product_info":
        return "product_info"

    if intent == "cart_action":
        return "cart_management"

    return "general_chat"



def route_from_general_chat(state: GraphState):
    sub_intent = state.get("sub_intent", "normal_chat")
    print(f"🔄 ROUTER: General chat sub-intent: {sub_intent}")
    return sub_intent

def route_after_product(state: GraphState):
    # Check if user wants to add to cart after seeing product
    last_message = state.get("messages", [])[-1]["content"].lower() if state.get("messages") else ""
    
    if "add" in last_message or "cart" in last_message:
        print(f"🔄 ROUTER: Product -> Cart (based on message: {last_message})")
        return "cart_management"
    
    # Or check cart action in state
    if state.get("cart_action") == "add":
        return "cart_management"
    
    print(f"🔄 ROUTER: Product -> Summarizer")
    return "summarizer"

def route_after_cart(state: GraphState):
    ctx = state.get("context", {})
    
    print(f"🔄 ROUTER: After cart - awaiting_quantity: {state.get('awaiting_quantity')}")
    print(f"🔄 ROUTER: After cart - requires_prescription: {state.get('requires_prescription')}")
    
    # 🔥 If we're asking for quantity, go to summarizer (graph completes)
    if state.get("awaiting_quantity"):
        print(f"🔄 ROUTER: Cart -> Summarizer (awaiting user input)")
        return "summarizer"
    
    # If prescription is required
    if state.get("requires_prescription"):
        print(f"🔄 ROUTER: Cart -> Prescription")
        return "prescription"
    
    # Otherwise go to summarizer
    print(f"🔄 ROUTER: Cart -> Summarizer (default)")
    return "summarizer"


def route_after_prescription(state: GraphState):
    # After prescription verification
    if state.get("prescription_status") == "verified":
        print(f"🔄 ROUTER: Prescription -> Cart (prescription verified, awaiting quantity)")
        return "cart_management"
    
    print(f"🔄 ROUTER: Prescription -> Summarizer")
    return "summarizer"


# ---------------- BUILD ----------------

def build_workflow():

    g = StateGraph(GraphState, reducers=STATE_REDUCERS)

    # Add all nodes
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

    # From supervisor
    g.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {
            "general_chat": "general_chat",
            "product_info": "product_info",
            "cart_management": "cart_management",  # This matches the return value
        }
    )

    # From general chat
    g.add_conditional_edges(
        "general_chat",
        route_from_general_chat,
        {
            "faq": "faq",
            "drug_interaction": "drug_interaction",
            "normal_chat": "normal_chat",
        }
    )

    # Direct edges
    g.add_edge("faq", "summarizer")
    g.add_edge("drug_interaction", "summarizer")
    g.add_edge("normal_chat", "summarizer")

    # From product info
    g.add_conditional_edges(
        "product_info",
        route_after_product,
        {
            "cart_management": "cart_management",
            "summarizer": "summarizer",
        }
    )

    # From cart management
    g.add_conditional_edges(
        "cart_management",
        route_after_cart,
        {
            "prescription": "prescription",
            "cart_management": "cart_management",  # Allow self-loop for quantity input
            "summarizer": "summarizer",
        }
    )

    # From prescription
    g.add_conditional_edges(
        "prescription",
        route_after_prescription,
        {
            "cart_management": "cart_management",
            "summarizer": "summarizer",
        }
    )

    g.add_edge("summarizer", END)

    workflow = g.compile()
    
    # Generate visualization
    try:
        png_bytes = workflow.get_graph().draw_mermaid_png()
        with open("pharmacy_langgraph_fixed.png", "wb") as f:
            f.write(png_bytes)
        print("✅ LangGraph visualization saved as pharmacy_langgraph_fixed.png")
    except Exception as e:
        print(f"⚠️ Could not generate visualization: {e}")
    
    return workflow