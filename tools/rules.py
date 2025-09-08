import re
from typing import List, Dict, Optional
from state import RoleSpec, Slots

ROLE_PATTERNS = [
    (r"founding engineer", "Founding Engineer"),
    (r"\bgenai intern\b|\bai intern\b|\bml intern\b", "GenAI Intern"),
    (r"software engineer", "Software Engineer"),
    (r"data engineer", "Data Engineer"),
    (r"ml engineer|machine learning engineer", "ML Engineer"),
]

def detect_roles(text: str) -> List[RoleSpec]:
    t = text.lower()
    roles = []
    for pat, title in ROLE_PATTERNS:
        if re.search(pat, t):
            roles.append(RoleSpec(title=title))
    return roles

def clarifying_questions(slots: Slots) -> List[str]:
    qs = []
    if not slots.roles:
        qs.append("Which role(s) do you want to hire? (e.g., Founding Engineer, GenAI Intern)")
    if not slots.budget:
        qs.append("What is your budget range? (e.g., $160k–$200k base + equity / $25–$35 per hour)")
    if not slots.timeline:
        qs.append("What is your hiring timeline? (e.g., 4–6 weeks)")
    if not slots.location:
        qs.append("Is the role remote, hybrid, or onsite?")
    if not slots.hiring_type:
        qs.append("Is this full-time, intern, or contract?")
    return qs[:3]

def jd_from_template(role: RoleSpec, slots: Slots) -> str:
    comp = slots.budget or "Compensation: TBD"
    return f"""### {role.title}

**Summary**  
We’re hiring a {role.title} to help build and scale our early product.

**Responsibilities**
- Own key features end-to-end
- Collaborate with founders and cross-functional partners
- Write clean, testable code and ship quickly
- Improve reliability, performance, and security
- Contribute to team processes and documentation

**Requirements (Must-have)**
- Solid Python/JavaScript (or relevant stack)
- Strong problem solving; ability to move fast with quality
- Communication skills and ownership mindset

**Nice-to-have**
- Startup or 0→1 experience
- GenAI/LangChain/LangGraph familiarity

**{comp}**  
**Apply:** careers@example.com
"""

def hiring_checklist(slots: Slots) -> List[Dict[str, str]]:
    return [
        {"stage": "Intake", "owner": "HR", "exit": "JD approved"},
        {"stage": "Sourcing", "owner": "Recruiter", "exit": "10 qualified candidates"},
        {"stage": "Screening", "owner": "HR", "exit": "Shortlist confirmed"},
        {"stage": "Technical", "owner": "Engineering", "exit": "Tech evaluation complete"},
        {"stage": "Culture/Founder", "owner": "Founder", "exit": "Culture fit approved"},
        {"stage": "Offer", "owner": "HR", "exit": "Offer accepted"},
        {"stage": "Onboarding", "owner": "Manager", "exit": "Hired onboarded"},
    ]

def kickoff_email(roles: List[RoleSpec], timeline: Optional[str], budget: Optional[str]) -> str:
    roles_txt = ", ".join([r.title for r in roles]) or "TBD"
    t = timeline or "TBD"
    b = budget or "TBD"
    return f"""Subject: Hiring Plan Kickoff

Hi Team,

We are planning to hire for: {roles_txt}
Timeline: {t}
Budget: {b}

Next Steps:
1) Finalize Job Descriptions
2) Begin Sourcing
3) Schedule Interviews

Thanks,
HR Agent
"""
