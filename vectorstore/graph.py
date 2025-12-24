from langgraph.graph import StateGraph, END
from state import PharmacyState

from nodes.router import router_node
from nodes.retriever import retriever_node
from nodes.responder import responder_node
from nodes.safety import safety_node
from nodes.escalation import escalation_node
from conditions import safety_condition

graph = StateGraph(PharmacyState)

graph.add_node("router", router_node)
graph.add_node("retriever", retriever_node)
graph.add_node("responder", responder_node)
graph.add_node("safety", safety_node)
graph.add_node("escalate", escalation_node)

graph.set_entry_point("router")

graph.add_edge("router", "retriever")
graph.add_edge("retriever", "responder")
graph.add_edge("responder", "safety")

graph.add_conditional_edges(
    "safety",
    safety_condition,
    {
        "escalate": "escalate",
        "end": END
    }
)

graph.add_edge("escalate", END)

app = graph.compile()
