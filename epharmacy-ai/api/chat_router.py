from fastapi import APIRouter
from pydantic import BaseModel

from graph.workflow import app
from evaluation.hallucination_check import hallucination_check
from evaluation.confidence_score import compute_confidence

router = APIRouter(prefix="/chat", tags=["AI Chat"])

class ChatRequest(BaseModel):
    query: str
    user_profile: dict = {}

@router.post("/")
def chat_endpoint(req: ChatRequest):
    state = {
        "user_query": req.query,
        "user_profile": req.user_profile,
        "agent_outputs": {},
        "safety_flags": []
    }

    result = app.invoke(state)

    hallucinated = hallucination_check(result)


    confidence = compute_confidence(
        result.get("retrieved_docs", []),
        result.get("risk_level", "LOW")
    )

    return {
        "answer": result["final_answer"],
        "confidence": confidence,
        "risk_level": result.get("risk_level"),
        "safety_flags": result.get("safety_flags"),
        "hallucination_detected": hallucinated
    }
