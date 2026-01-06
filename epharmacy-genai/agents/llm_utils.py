from tools.web_search_tool import web_search

def call_llm(prompt: str) -> str:
    """
    Unified LLM call wrapper using Groq backend.
    """

    result = web_search(prompt)

    if result["status"] == "success":
        return result["data"]["content"]

    # safe fallback
    return "I’m sorry, I couldn’t process that right now. Please try again later."
