from typing import Dict, List
from graph.state import GraphState
from agents.product_query_parser import extract_query_intent
from tools.postgres_tool import (
    fetch_product_with_stock,
    fetch_products_by_category_with_stock,
    fetch_all_categories,
    fuzzy_search_products
)
from agents.category_resolver import resolve_category


def product_info_node(state: GraphState) -> Dict:
    query = state["messages"][-1]["content"]

    # -----------------------------
    # 1️⃣ SEMANTIC EXTRACTION
    # -----------------------------
    params = extract_query_intent(query) or {}
    params.setdefault("products", [])
    params.setdefault("category", None)
    params.setdefault("alternatives", False)

    # -----------------------------
    # 2️⃣ CATEGORY RESOLUTION (DB-GROUNDED)
    # -----------------------------
    if params.get("category"):
        cats = fetch_all_categories()
        if cats["status"] == "success":
            match = resolve_category(params["category"], cats["data"])

            if match["matched_category"]:
                if match["confidence"] >= 0.5:
                    params["category"] = match["matched_category"]
                # else → keep original category phrase

    results: List[Dict] = []

    # -----------------------------
    # 3️⃣ STRATEGY 1 — EXACT PRODUCTS
    # -----------------------------
    for name in params.get("products", []):
        res = fetch_product_with_stock(name)
        if res["status"] == "success":
            results.append(res["data"])

    # -----------------------------
    # 4️⃣ STRATEGY 2 — CATEGORY SEARCH
    # -----------------------------
    if not results and params.get("category"):
        res = fetch_products_by_category_with_stock(params["category"])
        if res["status"] == "success":
            results.extend(res["data"])

    # -----------------------------
    # 4️⃣b RECOVERY CATEGORY SEARCH
    # -----------------------------
    if not results:
        cats = fetch_all_categories()
        if cats["status"] == "success":
            match = resolve_category(query, cats["data"])
            if match["matched_category"]:
                res = fetch_products_by_category_with_stock(match["matched_category"])
                if res["status"] == "success":
                    results.extend(res["data"])

    # -----------------------------
    # 5️⃣ HANDLE RESULTS
    # -----------------------------
    if results:
        return format_product_response(results)

    fuzzy = fuzzy_search_products(query)

    if fuzzy["status"] == "success" and fuzzy["data"]:
        return format_product_response(fuzzy["data"])

    # -----------------------------
    # 6️⃣ FALLBACK
    # -----------------------------
    return {
        "final_answer": (
            "I couldn’t find a matching product. "
            "Try searching by brand name (e.g., Crocin) or by category like "
            "'fever medicine' or 'cold relief'."
        )
    }


def format_product_response(products: List[Dict]) -> Dict:
    top = products[:3]

    lines = []
    for p in top:
        stock_msg = "In stock" if p["stock_qty"] > 0 else "Out of stock"
        rx = "Prescription required" if p["requires_prescription"] else "OTC"

        lines.append(
            f"- {p['name']} — ₹{p['price']} ({rx}, {stock_msg})"
        )

    return {
        "final_answer": "Here are some options:\n" + "\n".join(lines),
        "product_data": top,
        "requires_prescription": any(p["requires_prescription"] for p in top),
    }
