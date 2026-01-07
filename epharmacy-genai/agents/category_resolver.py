import json
from agents.llm_utils import call_llm

def resolve_category(user_term: str, categories: list):
    """
    Map user category phrase to the closest real DB category.
    """
    cat_list = ", ".join([c["name"] for c in categories])

    prompt = f"""
You are mapping a user request to a pharmacy category.

User phrase: "{user_term}"

Available categories:
{cat_list}

Return ONLY JSON:
{{
  "matched_category": "<one of the category names>",
  "confidence": 0.0-1.0
}}

If nothing fits well, return:
{{
  "matched_category": null,
  "confidence": 0.0
}}
"""

    try:
        raw = call_llm(prompt)
        data = json.loads(raw)
        return data
    except Exception:
        return {"matched_category": None, "confidence": 0.0}
