from state import AgentState
from tools.rules import jd_from_template

def jd_generator_node(state: AgentState) -> AgentState:
    jds = {}
    for role in state.slots.roles:
        jds[role.title] = jd_from_template(role, state.slots)
    state.artifacts.jds = jds
    return state
