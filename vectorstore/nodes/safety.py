from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

def safety_node(state):
    prompt = f"""
Answer: 
{state['answer']}

If unsafe respond ONLY with UNSAFE
Otherwise respond SAFE
"""
    safety = llm.invoke(prompt).content.strip()
    return {"safety": safety}
