from state import AgentState

def presenter_node(state: AgentState) -> AgentState:
    md = ["## Hiring Assistant Results"]
    if state.pending_questions:
        md.append("### Clarifying Questions")
        md.extend([f"- {q}" for q in state.pending_questions])
    if state.artifacts.jds:
        md.append("\n### Job Descriptions")
        for title, jd in state.artifacts.jds.items():
            md.append(f"\n{jd}")
    if state.artifacts.plan_markdown:
        md.append("\n### Hiring Plan")
        md.append(state.artifacts.plan_markdown)
    if state.artifacts.email_draft:
        md.append("\n### Draft Email\n```\n" + state.artifacts.email_draft + "\n```")
    state.artifacts.result_markdown = "\n".join(md)
    return state
