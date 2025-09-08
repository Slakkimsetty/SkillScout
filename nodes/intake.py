from state import AgentState
from tools.rules import detect_roles

def intake_node(state: AgentState) -> AgentState:
    if state.user_query and not state.slots.roles:
        detected = detect_roles(state.user_query)
        if detected:
            state.slots.roles = detected
    return state
