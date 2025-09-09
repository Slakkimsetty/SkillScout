# nodes/email_writer.py
from tools.email_tool import kickoff_email
from state import AgentState

def email_writer_node(state: AgentState) -> AgentState:
    roles_payload = [{"title": r.title} for r in state.slots.roles]
    state.artifacts.email_draft = kickoff_email(roles_payload, state.slots.budget, state.slots.timeline)
    return state
