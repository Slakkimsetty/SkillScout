# nodes/clarifier.py
from state import AgentState

NEEDED = ["budget", "timeline", "location", "hiring_type"]

def clarifier_node(state: AgentState) -> AgentState:
    missing = []
    s = state.slots
    if not s.budget: missing.append("What’s your budget range?")
    if not s.timeline: missing.append("What’s the hiring timeline?")
    if not s.location: missing.append("Is the role remote, hybrid or onsite?")
    if not s.hiring_type: missing.append("Is this full-time, intern, or contract?")
    # store a quick summary markdown for UI
    if missing:
        state.artifacts.summary_md = "### Clarifying Questions\n" + "\n".join([f"- {q}" for q in missing])
    else:
        state.artifacts.summary_md = "### Clarifying Questions\n- All set (no blockers)."
    return state
