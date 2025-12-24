from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3
)

def responder_node(state):
    context = "\n\n".join(state["documents"])

    prompt = f"""
You are a pharmacy assistant.
Answer ONLY using the context below.
Do NOT guess.

Context:
{context}

Question:
{state['query']}
"""

    answer = llm.invoke(prompt).content
    return {"answer": answer}
