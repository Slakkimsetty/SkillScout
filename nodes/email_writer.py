from state import AgentState
from tools.rules import kickoff_email

def email_writer_node(state: AgentState) -> AgentState:
    state.artifacts.email_draft = kickoff_email(
        roles=state.slots.roles,
        timeline=state.slots.timeline,
        budget=state.slots.budget,
    )
    return state
