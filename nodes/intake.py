# nodes/intake.py
import re
from typing import List
from state import AgentState, RoleSpec

ROLE_ALIASES = {
    "founding engineer": ["founding engineer", "founder engineer", "first engineer"],
    "genai intern": ["genai intern", "ai intern", "ml intern", "gen ai intern"],
    "ml engineer": ["ml engineer", "machine learning engineer", "ml eng"],
    "devops/sre": ["devops", "sre", "site reliability"]
}

def detect_roles(text: str) -> List[RoleSpec]:
    roles: List[RoleSpec] = []
    t = text.lower()
    matched = False
    for canonical, keys in ROLE_ALIASES.items():
        if any(k in t for k in keys):
            title = canonical.title()
            roles.append(RoleSpec(title=title))
            matched = True
    if not matched:
        roles.append(RoleSpec(title="Software Engineer (Startup)"))
    return roles

def extract_slots(text: str, state: AgentState) -> AgentState:
    t = text.lower()
    # budget
    m = re.search(r'(\$\s?\d[\d,]*\s?(k|/hr|k\+)?|\d+\s?lpa|\$\s?\d+\s?-\s?\$\s?\d+)', t)
    if m and not state.slots.budget:
        state.slots.budget = m.group(0).replace(" ", "")
    # timeline
    m = re.search(r'(\d+\s?(weeks?|months?))|(next\s?\d+\s?(weeks?|months?))', t)
    if m and not state.slots.timeline:
        state.slots.timeline = m.group(0)
    # location
    for loc in ["remote","hybrid","onsite"]:
        if loc in t and not state.slots.location:
            state.slots.location = loc.title()
            break
    # type
    for ty in ["full-time","contract","intern","internship"]:
        if ty in t and not state.slots.hiring_type:
            state.slots.hiring_type = "intern" if "intern" in ty else ty.title()
            break
    # skills hint
    skill_hits = [s for s in ["python","aws","kubernetes","terraform","vector","prompt","react","node"] if s in t]
    state.slots.skills_hint = sorted(set(state.slots.skills_hint + skill_hits))
    return state

def intake_node(state: AgentState) -> AgentState:
    if not state.slots.roles:
        state.slots.roles = detect_roles(state.user_query)
    state = extract_slots(state.user_query, state)
    return state
