import json
import os
import time
from typing import Optional, Dict
from graph.state import GraphState

CHECKPOINT_DIR = "memory/checkpoints"
CHECKPOINT_TTL_SECONDS = 24 * 60 * 60  # 24 hours


# -----------------------------
# UTILITIES
# -----------------------------

def _ensure_dir():
    if not os.path.exists(CHECKPOINT_DIR):
        os.makedirs(CHECKPOINT_DIR)


def _checkpoint_path(conversation_id: str) -> str:
    return os.path.join(CHECKPOINT_DIR, f"{conversation_id}.json")


# -----------------------------
# CORE CHECKPOINTER
# -----------------------------

class FileCheckpointer:
    """
    Simple file-based checkpointer for:
    - pause / resume
    - human-in-loop
    - crash recovery
    """

    def __init__(self):
        _ensure_dir()

    # -------------------------
    # SAVE
    # -------------------------
    def save(
        self,
        conversation_id: str,
        state: GraphState,
        current_node: str
    ) -> None:
        payload = {
            "conversation_id": conversation_id,
            "current_node": current_node,
            "state": state,
            "timestamp": time.time()
        }

        with open(_checkpoint_path(conversation_id), "w") as f:
            json.dump(payload, f, indent=2)

    # -------------------------
    # LOAD
    # -------------------------
    def load(
        self,
        conversation_id: str
    ) -> Optional[Dict]:
        path = _checkpoint_path(conversation_id)
        if not os.path.exists(path):
            return None

        with open(path, "r") as f:
            return json.load(f)

    # -------------------------
    # DELETE
    # -------------------------
    def delete(self, conversation_id: str) -> None:
        path = _checkpoint_path(conversation_id)
        if os.path.exists(path):
            os.remove(path)

    # -------------------------
    # CLEANUP
    # -------------------------
    def cleanup_expired(self) -> None:
        """
        Remove checkpoints older than TTL.
        """
        now = time.time()
        for file in os.listdir(CHECKPOINT_DIR):
            if not file.endswith(".json"):
                continue

            path = os.path.join(CHECKPOINT_DIR, file)
            try:
                with open(path, "r") as f:
                    payload = json.load(f)
                ts = payload.get("timestamp", 0)

                if now - ts > CHECKPOINT_TTL_SECONDS:
                    os.remove(path)
            except Exception:
                # If corrupted, delete it
                os.remove(path)

    def resume_from_checkpoint(self, conversation_id: str):
        data = self.load(conversation_id)
        if not data:
            return None

        return {
            "state": data["state"],
            "current_node": data["current_node"]
        }


