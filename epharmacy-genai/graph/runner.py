from graph.workflow import build_workflow
from memory.checkpointer import FileCheckpointer
from agents.memory_curator import extract_memory_notes

class WorkflowRunner:
    def __init__(self):
        self.workflow = build_workflow()
        self.checkpointer = FileCheckpointer()

    def run(self, state, conversation_id: str):
        # -----------------------------
        # RUN GRAPH
        # -----------------------------
        new_state = self.workflow.invoke(state)

        # -----------------------------
        # 🧠 LLM-MANAGED SHORT-TERM MEMORY
        # -----------------------------
        try:
            user_msg = state["messages"][-1]["content"]
            bot_msg = new_state.get("final_answer", "")

            notes = extract_memory_notes(user_msg, bot_msg)

            if notes:
                new_state.setdefault("memory_notes", [])
                new_state["memory_notes"].extend(notes)

                # cap memory
                MAX_NOTES = 20
                if len(new_state["memory_notes"]) > MAX_NOTES:
                    new_state["memory_notes"] = new_state["memory_notes"][-MAX_NOTES:]

        except Exception:
            # memory failure must NEVER break chat
            pass

        # -----------------------------
        # SAVE CHECKPOINT
        # -----------------------------
        self.checkpointer.save(
            conversation_id=conversation_id,
            state=new_state,
            current_node="END"
        )

        return new_state
