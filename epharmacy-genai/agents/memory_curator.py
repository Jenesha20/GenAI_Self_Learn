from agents.llm_utils import call_llm

def extract_memory_notes(user_msg: str, bot_msg: str):
    prompt = f"""
You are managing short-term conversational memory.

Conversation turn:
User: {user_msg}
Assistant: {bot_msg}

Decide if there is anything important to remember for this session.
Examples of useful memory:
- preferences
- allergies
- repeated interests
- ongoing tasks

If nothing important, return: NONE
Otherwise, return 1–2 short bullet points.
"""

    result = call_llm(prompt)

    if result.strip().upper() == "NONE":
        return []

    # split bullets safely
    notes = [n.strip("- ").strip() for n in result.split("\n") if n.strip()]
    return notes
