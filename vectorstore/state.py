from typing import TypedDict, List

class PharmacyState(TypedDict):
    query: str
    intent: str
    documents: List[str]
    answer: str
    safety: str
