from graph.state import get_default_state
from memory.checkpointer import FileCheckpointer
from graph.runner import WorkflowRunner
import uuid
from graph.state_utils import reset_control_state

def run_chatbot():
    print("\n🩺 E-Pharmacy Support Bot")
    print("Type 'exit' to quit.\n")

    conversation_id = "terminal-session"   # stable session
    checkpointer = FileCheckpointer()
    runner = WorkflowRunner()

    # -----------------------------
    # RESTORE OR CREATE STATE
    # -----------------------------
    checkpoint = checkpointer.load(conversation_id)

    if checkpoint:
        print("🔁 Restoring previous session...\n")
        state = checkpoint["state"]
    else:
        state = get_default_state()
        state["user_id"] = "terminal_user"
        state["conversation_id"] = conversation_id

    # -----------------------------
    # CHAT LOOP
    # -----------------------------
    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Bot: Goodbye! 👋")
            break

       # store user message
        state["messages"].append({
            "role": "user",
            "content": user_input
        })

        # 🔥 RESET CONTROL STATE (keep memory, reset flow)
        state = reset_control_state(state)

        # run workflow + checkpoint
        state = runner.run(state, conversation_id)


        print("Bot:", state.get("final_answer", "I couldn't process that."))


if __name__ == "__main__":
    run_chatbot()
