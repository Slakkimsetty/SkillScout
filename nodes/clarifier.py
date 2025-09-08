from state import AgentState
from tools.rules import clarifying_questions

def clarifier_node(state: AgentState) -> AgentState:
    qs = clarifying_questions(state.slots)
    state.pending_questions = qs
    state.awaiting_answers = len(qs) > 0
    return state
