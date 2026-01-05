from langgraph.graph import StateGraph
from graph.state import GraphState

from graph.nodes.intent_node import intent_classifier
from graph.nodes.safety_node import safety_agent
from graph.nodes.retrieval_node import retrieval_agent
from graph.nodes.clinical_node import clinical_agent
from graph.nodes.final_node import final_answer_node

graph = StateGraph(GraphState)

# ---- Nodes ----
graph.add_node("intent", intent_classifier)
graph.add_node("safety", safety_agent)
graph.add_node("retrieval", retrieval_agent)
graph.add_node("clinical", clinical_agent)
graph.add_node("final", final_answer_node)

# ---- Entry ----
graph.set_entry_point("intent")

# ---- Flow ----
graph.add_edge("intent", "safety")

def route_after_safety(state: GraphState):
    if state.get("is_safety_refusal"):
        return "final"
    return "retrieval"

graph.add_conditional_edges(
    "safety",
    route_after_safety,
    {
        "final": "final",
        "retrieval": "retrieval"
    }
)



graph.add_edge("retrieval", "clinical")
graph.add_edge("clinical", "final")

app = graph.compile()
