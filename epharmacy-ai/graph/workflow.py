from langgraph.graph import StateGraph
from graph.state import GraphState

from graph.nodes.intent_node import intent_classifier
from graph.nodes.safety_node import safety_agent
from graph.nodes.retrieval_node import retrieval_agent
from graph.nodes.clinical_node import clinical_agent
from graph.nodes.final_node import final_answer_node
from graph.nodes.web_node import web_agent

graph = StateGraph(GraphState)

# ---- Nodes ----
graph.add_node("intent", intent_classifier)
graph.add_node("safety", safety_agent)
graph.add_node("retrieval", retrieval_agent)
graph.add_node("clinical", clinical_agent)
graph.add_node("web", web_agent)
graph.add_node("final", final_answer_node)

# ---- Entry ----
graph.set_entry_point("intent")

# ---- Flow ----
graph.add_edge("intent", "safety")

def route_after_safety(state: GraphState):
    if state.get("is_safety_refusal"):
        return "final"
    return "retrieval"

def should_use_web(state: GraphState):
    docs = state.get("retrieved_docs", [])
    confidence = state.get("confidence_score", 0.0)

    if not docs:
        return True

    if confidence < 0.4:
        return True

    return False

graph.add_conditional_edges(
    "safety",
    route_after_safety,
    {
        "final": "final",
        "retrieval": "retrieval"
    }
)



graph.add_conditional_edges(
    "retrieval",
    lambda state: "web" if should_use_web(state) else "clinical",
    {
        "web": "web",
        "clinical": "clinical"
    }
)
graph.add_edge("web", "clinical")
graph.add_edge("clinical", "final")

app = graph.compile()

png_bytes = app.get_graph().draw_mermaid_png()

with open("pharmacy_langgraph.png", "wb") as f:
    f.write(png_bytes)

print("LangGraph visualization saved as pharmacy_langgraph.png")
