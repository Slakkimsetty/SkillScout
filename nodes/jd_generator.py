# nodes/jd_generator.py — JD in your example’s structure (Python 3.9–safe)
from typing import List, Optional
import yaml
from pathlib import Path
from state import AgentState, RoleSpec

ROLE_DATA = yaml.safe_load(Path("data/roles.yml").read_text(encoding="utf-8"))

# -------- helpers --------
def _cap(s: str) -> str:
    s = (s or "").strip()
    if not s: return ""
    return s[0].upper() + s[1:] if s[0].islower() else s

def _sent(s: str) -> str:
    s = _cap(s)
    if s and s[-1] not in ".!?":
        s += "."
    return s

def _bulletize(items: List[str]) -> str:
    """Return a markdown bullet list from sentences."""
    clean = [ _sent(x) for x in items if x and x.strip() ]
    if not clean:
        return "- (none)"
    return "\n".join(["- " + x for x in clean])

def _infer_duration_phrase(timeline: Optional[str], hiring_type: Optional[str]) -> Optional[str]:
    if not timeline and not hiring_type:
        return None
    if timeline and hiring_type and hiring_type.lower() in {"intern", "contract"}:
        return f"{timeline} {hiring_type.lower()}"
    if timeline:
        return timeline
    return hiring_type

def _normalize_skill_sentence(s: str) -> str:
    ss = s.strip()
    if " " not in ss and ss.isalpha():
        return f"Proficiency in {ss.capitalize()}."
    return _sent(ss)

# -------- JD composer --------
def _compose_jd(
    role: RoleSpec,
    skills_hint: List[str],
    company_name: Optional[str],
    location: Optional[str],
    timeline: Optional[str],
    budget: Optional[str],
    hiring_type: Optional[str],
) -> str:
    data = ROLE_DATA.get(role.title, ROLE_DATA.get("Founding Engineer", {}))

    # seeds
    summary = data.get("summary", "")
    resp_seed = list(data.get("responsibilities", []))
    must_seed = list(data.get("must_have", []))
    nice_seed = list(data.get("nice_to_have", []))

    # merge skills into requirements (dedup, keep order)
    if skills_hint:
        for s in skills_hint:
            if s not in must_seed:
                must_seed.append(s)

    # craft lines (professional)
    company = company_name or "Our company"
    loc_line = location or "Remote/Hybrid/Onsite (to be confirmed)"
    duration_phrase = _infer_duration_phrase(timeline, hiring_type)

    # Company Overview (two sentences is fine)
    co_lines = [
        f"{company} is dedicated to building innovative, AI-driven solutions for real customers.",
        "We foster a collaborative, inclusive environment where ownership, learning, and delivery matter.",
    ]
    if duration_phrase and hiring_type and hiring_type.lower() in {"intern", "contract"}:
        co_lines.append(f"We are seeking a motivated {role.title} to join the team on a {duration_phrase} basis.")

    # Job Description (mix summary + skills + hiring type)
    jd_lines = []
    if summary:
        jd_lines.append(summary)
    if hiring_type and hiring_type.lower() in {"intern", "contract"} and not duration_phrase:
        jd_lines.append(f"This is a {hiring_type.lower()} role.")
    if skills_hint:
        jd_lines.append("The ideal candidate is comfortable with " + ", ".join([s.upper() if s.lower() in {"gcp","aws","azure"} else s for s in skills_hint]) + ".")

    # Responsibilities (ensure full sentences)
    resp_lines = [ _sent(x) for x in resp_seed ]
    # add a couple sensible, professional items if missing
    extras = []
    if "python" in [s.lower() for s in skills_hint]:
        extras.append("Write clean, well-documented Python code and contribute to code reviews.")
    if any(s.lower() in {"gcp","aws","azure"} for s in skills_hint):
        extras.append("Utilize cloud services to develop, deploy, and monitor AI workloads in a secure and cost-efficient manner.")
    if extras:
        resp_lines.extend(extras)

    # Qualifications (must + nice) → bullets
    qual_lines = [ _normalize_skill_sentence(m) for m in must_seed ] + [ _normalize_skill_sentence(n) for n in nice_seed ]

    # Benefits (generic but professional)
    if hiring_type and hiring_type.lower() in {"intern", "contract"}:
        benefits = [
            "Gain hands-on experience delivering scoped outcomes with close mentorship.",
            "Work on real-world AI projects with clear learning objectives.",
            "Flexible working hours and the ability to work remotely.",
            "Competitive, market-informed compensation.",
        ]
    else:
        benefits = [
            "A culture of ownership and impact with early product influence.",
            "Opportunities for growth, mentorship, and continuous learning.",
            "Flexible work arrangements, including remote options.",
            "Competitive, market-informed compensation.",
        ]

    # Build the final JD text (Markdown)
    parts = []
    parts.append(f"**Job Title:** {role.title}")
    parts.append(f"**Location:** {loc_line}")
    if duration_phrase:
        parts.append(f"**Duration:** {duration_phrase}")
    if budget:
        parts.append(f"**Budget:** {budget}")
    parts.append("")  # blank line

    parts.append("**Company Overview:**")
    parts.append(" ".join([_sent(l) for l in co_lines]))
    parts.append("")

    parts.append("**Job Description:**")
    jd_text = " ".join([_sent(l) for l in jd_lines]) if jd_lines else "We are looking for a motivated professional to contribute to high-impact initiatives."
    parts.append(jd_text)
    parts.append("")

    parts.append("**Responsibilities:**")
    parts.append(_bulletize(resp_lines))
    parts.append("")

    parts.append("**Qualifications:**")
    parts.append(_bulletize(qual_lines))
    parts.append("")

    parts.append("**Benefits:**")
    parts.append(_bulletize(benefits))
    parts.append("")

    parts.append("**How to Apply:**")
    parts.append("Please submit your resume (and portfolio or GitHub, if relevant). Include a brief note on your availability and the most relevant project you have built.")
    parts.append("")

    return "\n".join(parts)

def jd_generator_node(state: AgentState) -> AgentState:
    skills = state.slots.skills_hint or []
    company = state.slots.company_name
    loc = state.slots.location
    tline = state.slots.timeline
    budg = state.slots.budget
    htype = state.slots.hiring_type

    for role in state.slots.roles:
        md = _compose_jd(
            role=role,
            skills_hint=skills,
            company_name=company,
            location=loc,
            timeline=tline,
            budget=budg,
            hiring_type=htype,
        )
        state.artifacts.jds[role.title] = md

    state.analytics["roles_created"] = len(state.artifacts.jds)
    return state
