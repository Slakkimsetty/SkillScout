# nodes/presenter.py
from state import AgentState

def presenter_node(state: AgentState) -> AgentState:
    # Compose a single markdown for easy download
    parts = [f"# Hiring Assistant Results",
             state.artifacts.summary_md,
             "## Job Descriptions"]
    for title, md in state.artifacts.jds.items():
        parts.append(md)
    parts.append(state.artifacts.plan_markdown)
    if state.artifacts.email_draft:
        parts.append("## Kickoff Email\n```\n"+state.artifacts.email_draft+"\n```")
    state.artifacts.summary_md = "\n\n".join(parts)
    return state
