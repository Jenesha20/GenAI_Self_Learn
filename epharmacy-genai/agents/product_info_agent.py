import re
from graph.state import GraphState
from tools.postgres_tool import fetch_product_info

def extract_product_name(text: str) -> str:
    text = text.lower()
    text = re.sub(r"(give me|show me|tell me|about|product|info|details|buy|add)", "", text)
    return text.strip()

def product_info_node(state: GraphState) -> GraphState:
    raw_query = state["messages"][-1]["content"]
    product_name = extract_product_name(raw_query)

    result = fetch_product_info(product_name)

    if result["status"] == "success":
        return {
            "product_data": result["data"],
            "requires_prescription": result["data"]["requires_prescription"]
        }

    return {
        "final_answer": "Product not found. Please try again."
    }
