from graph.workflow import build_workflow
from memory.checkpointer import FileCheckpointer

class WorkflowRunner:
    def __init__(self):
        self.workflow = build_workflow()
        self.checkpointer = FileCheckpointer()

    def run(self, state, conversation_id: str):
        # run graph
        new_state = self.workflow.invoke(state)

        # save checkpoint
        self.checkpointer.save(
            conversation_id=conversation_id,
            state=new_state,
            current_node="END"
        )

        return new_state
