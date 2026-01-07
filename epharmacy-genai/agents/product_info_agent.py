import re
from graph.state import GraphState
from tools.postgres_tool import fetch_product_info, fetch_products_by_category

CATEGORY_PATTERNS = [
    r"products? for (.*)",
    r"medicines? for (.*)",
    r"meds for (.*)",
]

def extract_product_or_category(text: str):
    text = text.lower()

    for p in CATEGORY_PATTERNS:
        m = re.search(p, text)
        if m:
            return ("category", m.group(1).strip())

    # fallback → single product
    cleaned = re.sub(
        r"(give me|show me|tell me|about|product|info|details|buy|add)",
        "",
        text,
    )
    return ("product", cleaned.strip())


def product_info_node(state: GraphState) -> dict:
    raw_query = state["messages"][-1]["content"]
    kind, value = extract_product_or_category(raw_query)

    # -----------------------------
    # 1️⃣ Category flow
    # -----------------------------
    if kind == "category":
        result = fetch_products_by_category(value)

        if result["status"] == "success" and result["data"]:
            products = result["data"]
            names = ", ".join(p["name"] for p in products[:5])

            return {
                "final_answer": (
                    f"For {value}, we currently have: {names}. "
                    "Would you like details for any of these?"
                )
            }

        return {
            "final_answer": f"Sorry, I couldn’t find products for {value}."
        }

    # -----------------------------
    # 2️⃣ Single product flow
    # -----------------------------
    result = fetch_product_info(value)

    if result["status"] == "success":
        return {
            "product_data": result["data"],
            "requires_prescription": result["data"]["requires_prescription"]
        }

    return {
        "final_answer": "Sorry, I couldn’t find that product."
    }
