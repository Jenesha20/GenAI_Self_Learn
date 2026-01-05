from typing import TypedDict, List, Optional

class GraphState(TypedDict, total=False):
    user_query: str
    user_profile: dict

    intent: Optional[str]

    # 🔥 MUST BE PRESENT
    risk_level: Optional[str]
    safety_flags: List[str]
    is_safety_refusal: bool

    retrieved_docs: list
    agent_outputs: dict

    final_answer: Optional[str]
    confidence_score: Optional[float]
