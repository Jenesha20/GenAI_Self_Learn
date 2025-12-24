from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

def router_node(state):
    prompt = f"""
Classify this pharmacy query into ONE category only:
drug_info
dosage
interaction
prescription_required
general

Query: {state['query']}
"""

    intent = llm.invoke(prompt).content.strip().lower()
    return {"intent": intent}
