from state import AgentState
from tools.rules import hiring_checklist

def plan_builder_node(state: AgentState) -> AgentState:
    checklist = hiring_checklist(state.slots)
    state.artifacts.plan_json = checklist
    state.artifacts.plan_markdown = "\n".join(
        [f"- {c['stage']} (Owner: {c['owner']}, Exit: {c['exit']})" for c in checklist]
    )
    return state
