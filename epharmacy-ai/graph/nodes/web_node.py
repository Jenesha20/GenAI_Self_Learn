import os
from groq import Groq
from graph.state import GraphState

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def web_agent(state: GraphState) -> GraphState:
    query = state["user_query"]

    prompt = f"""
You are a medical information assistant.
Answer the following query using general medical knowledge.
Be factual, safe, and concise.
If the query is risky, advise consulting a doctor.

Query: {query}

Provide:
1. A short medical answer
2. 2 trusted source names (not URLs)
"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You provide safe medical information."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        text = completion.choices[0].message.content

        state.setdefault("agent_outputs", {})
        state["agent_outputs"]["web"] = {
            "content": text,
            "sources": ["WHO", "Drugs.com"]
        }

        print("🌐 WEB AGENT EXECUTED")

    except Exception as e:
        state.setdefault("agent_outputs", {})
        state["agent_outputs"]["web"] = {
            "content": "Unable to fetch web information at this time.",
            "sources": []
        }
        print("❌ WEB AGENT ERROR:", e)

    return state
