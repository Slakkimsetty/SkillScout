# nodes/plan_builder.py
from tools.checklist_tool import build_checklist
from state import AgentState

def plan_to_markdown(items):
    out = ["## Hiring Plan"]
    for i, it in enumerate(items, 1):
        out.append(f"{i}. **{it['stage']}** — Owner: {it['owner']}; ETA: {it['eta_days']} days")
    return "\n".join(out)

def plan_builder_node(state: AgentState) -> AgentState:
    roles_payload = [{"title": r.title} for r in state.slots.roles]
    plan = build_checklist(roles_payload, state.slots.hiring_type)
    state.artifacts.plan_json = plan
    state.artifacts.plan_markdown = plan_to_markdown(plan)
    state.analytics["checklist_items"] = len(plan)
    return state
