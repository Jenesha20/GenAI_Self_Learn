from graph.state import GraphState
from tools.web_search_tool import web_search

def normal_chat_node(state: GraphState) -> GraphState:
    query = state["messages"][-1]["content"]
    result = web_search(query)

    if result["status"] == "success":
        return {
            "messages": [{
                "role": "assistant",
                "content": result["data"]["content"]
            }]
        }

    return {
        "final_answer": result["message"]
    }
