import json
from agents.llm_utils import call_llm

def extract_query_intent(query: str) -> dict:
    prompt = f"""
You are an assistant that extracts structured search intent for a pharmacy system.

From this user query, extract information and return ONLY valid JSON.

Fields (use null if not mentioned):
{{
  "products": [],              // list of product names mentioned
  "category": null,            // fever / cold / pain / allergy etc.
  "max_price": null,           // integer rupees
  "alternatives": false,       // true if user asks for substitutes
  "in_stock_only": true        // default true
}}

User query:
{query}
"""

    try:
        raw = call_llm(prompt)
        data = json.loads(raw)
        return data
    except Exception:
        # safe fallback
        return {
            "products": [],
            "category": None,
            "max_price": None,
            "alternatives": False,
            "in_stock_only": True,
        }
