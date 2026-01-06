import os
import requests
from typing import Dict

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

def web_search(query: str) -> Dict:
    """
    External LLM-backed web response for normal chat only.
    """
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ],
            "temperature": 0.3
        }

        r = requests.post(GROQ_ENDPOINT, headers=headers, json=payload, timeout=15)

        if r.status_code != 200:
            return {
                "status": "error",
                "data": None,
                "message": "External service error"
            }

        content = r.json()["choices"][0]["message"]["content"]

        return {
            "status": "success",
            "data": {"content": content},
            "message": "Response fetched"
        }

    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "message": str(e)
        }
