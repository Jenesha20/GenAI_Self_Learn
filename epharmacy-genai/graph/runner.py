from graph.workflow import build_workflow
from memory.checkpointer import FileCheckpointer
from agents.memory_curator import extract_memory_notes
from graph.context_resolver import resolve_context   # 🔥 NEW


class WorkflowRunner:
    def __init__(self):
        self.workflow = build_workflow()
        self.checkpointer = FileCheckpointer()

    def run(self, state, conversation_id: str):

        # ------------------------------------------------
        # 🔥 1. CONTEXT RESOLUTION (before routing)
        # ------------------------------------------------
        try:
            state = resolve_context(state)
        except Exception:
            # context resolution must NEVER break chat
            pass

        # ------------------------------------------------
        # 2. RUN GRAPH
        # ------------------------------------------------
        new_state = self.workflow.invoke(state)

        # ------------------------------------------------
        # 🧠 3. LLM-MANAGED SHORT-TERM MEMORY
        # ------------------------------------------------
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

        # ------------------------------------------------
        # 4. SAVE CHECKPOINT
        # ------------------------------------------------
        try:
            self.checkpointer.save(
                conversation_id=conversation_id,
                state=new_state,
                current_node="END"
            )
        except Exception:
            # checkpoint failure must NEVER break chat
            pass

        return new_state
