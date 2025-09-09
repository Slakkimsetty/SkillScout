# tools/checklist_tool.py
# Dynamic, professional hiring plans (Python 3.9–safe)

from typing import List, Dict, Optional

# ---------------- utilities ----------------
def _title_flags(roles: List[Dict]) -> Dict[str, bool]:
    """Infer role category signals from titles."""
    titles = [str(r.get("title", "")).lower() for r in roles]
    is_founding = any(any(k in t for k in ["founding", "founder", "first engineer"]) for t in titles)
    is_lead = any(any(k in t for k in ["lead", "principal", "staff", "head", "director"]) for t in titles)
    return {"founding": is_founding, "lead": is_lead}

def _dedup(stages: List[Dict]) -> List[Dict]:
    """Remove duplicate stage lines while preserving order."""
    seen = set()
    out: List[Dict] = []
    for s in stages:
        key = s.get("stage", "").strip().lower()
        if key and key not in seen:
            seen.add(key)
            out.append(s)
    return out

def _extras_common() -> List[Dict]:
    """Cross-functional touches that raise quality and fairness."""
    return [
        {"stage": "Run an inclusive language and DEI check on the job description and interview rubric.", "owner": "HR", "eta_days": 1},
        {"stage": "Provide interview training and rubric alignment for panelists.", "owner": "HR/Managers", "eta_days": 1},
        {"stage": "Set up candidate-experience SLAs (response times, feedback templates, scheduling flow).", "owner": "HR", "eta_days": 1},
        {"stage": "Enable basic analytics for funnel visibility (source quality, pass-through rates, time-to-hire).", "owner": "HR/OPS", "eta_days": 1},
        {"stage": "Collect post-hire feedback to improve the hiring process.", "owner": "HR/Managers", "eta_days": 1},
    ]

# ---------------- plan builders ----------------
def _plan_founding() -> List[Dict]:
    return [
        {"stage": "Define scope, ownership, and success metrics for the founding role; align equity philosophy.", "owner": "Founders/HR", "eta_days": 2},
        {"stage": "Draft and approve a founder-level job description and evaluation rubric.", "owner": "Founders/HR", "eta_days": 2},
        {"stage": "Activate targeted sourcing via networks, founder communities, and warm introductions.", "owner": "Founders/HR", "eta_days": 10},
        {"stage": "Run deep-dive founder interviews on vision alignment, risk appetite, and execution.", "owner": "Founders", "eta_days": 3},
        {"stage": "Evaluate technical leadership through a real product working session.", "owner": "Eng/Founders", "eta_days": 3},
        {"stage": "Calibrate compensation and equity; align with legal/finance.", "owner": "Founders/HR", "eta_days": 2},
        {"stage": "Conduct mutual reference checks (two-way).", "owner": "Founders/HR", "eta_days": 2},
        {"stage": "Present final proposal; negotiate and close with clear milestones.", "owner": "Founders/HR", "eta_days": 3},
        {"stage": "Plan onboarding into strategy, ownership areas, and first-90-day outcomes.", "owner": "Founders/HR", "eta_days": 2},
    ]

def _plan_intern_or_contract() -> List[Dict]:
    return [
        {"stage": "Define project scope, deliverables, and success criteria aligned to the engagement timeline.", "owner": "Eng/HR", "eta_days": 2},
        {"stage": "Draft and approve the role description emphasizing learning, mentorship, and outcomes.", "owner": "HR/Eng", "eta_days": 2},
        {"stage": "Source via campus channels, communities, and referrals; publish to selected boards.", "owner": "HR", "eta_days": 7},
        {"stage": "Screen for motivation and fundamentals; run a lightweight technical exercise.", "owner": "Eng", "eta_days": 3},
        {"stage": "Assign a mentor and prepare a starter project with clear checkpoints.", "owner": "Eng", "eta_days": 1},
        {"stage": "Offer, paperwork, and start-date confirmation.", "owner": "HR", "eta_days": 2},
        {"stage": "Execute fast onboarding (tools, data access, docs) and weekly demo cadence.", "owner": "Eng/HR", "eta_days": 2},
        {"stage": "Midpoint evaluation against scope; adjust plan if needed.", "owner": "Eng/HR", "eta_days": 1},
        {"stage": "Final presentation and wrap-up; capture learnings and next steps (conversion path if applicable).", "owner": "Eng/HR", "eta_days": 1},
    ]

def _plan_fulltime_standard(is_lead: bool) -> List[Dict]:
    return [
        {"stage": "Define role requirements, success metrics, and interview rubric.", "owner": "HR/Manager", "eta_days": 2},
        {"stage": "Draft and approve the job description and candidate profile.", "owner": "HR/Manager", "eta_days": 2},
        {"stage": "Publish to selected job boards and activate targeted sourcing/outreach.", "owner": "HR", "eta_days": 7},
        {"stage": "Structured resume screen using the rubric; shortlist for phone screen.", "owner": "HR/Manager", "eta_days": 3},
        {"stage": f"Run {'leadership + ' if is_lead else ''}technical evaluation (exercise or portfolio review).", "owner": "Eng/Manager", "eta_days": 5},
        {"stage": "Panel interviews with cross-functional peers; assess collaboration and ownership.", "owner": "Manager", "eta_days": 3},
        {"stage": "Reference checks and compensation calibration against market.", "owner": "HR/Manager", "eta_days": 2},
        {"stage": "Offer, negotiation, and close with agreed start date.", "owner": "HR/Manager", "eta_days": 3},
        {"stage": "Pre-onboarding checklist; assign buddy and 30/60/90-day plan.", "owner": "HR/Manager", "eta_days": 2},
    ]

# ---------------- public API ----------------
def build_checklist(roles: List[Dict], hiring_type: Optional[str]) -> List[Dict]:
    """
    Returns a professional, role-aware hiring plan.
    - Founding roles: founder-specific flow (equity, mutual references, strategy onboarding).
    - Intern/Contract: scope-first, mentorship, weekly demos, midpoint review, final presentation.
    - Full-time: structured rubric, panel loop, reference + calibration, 30/60/90 onboarding.
    Includes quality extras (DEI, interview training, candidate experience, analytics, post-hire feedback).
    """
    flags = _title_flags(roles)
    htype = (hiring_type or "").lower()

    if flags["founding"]:
        base = _plan_founding()
    elif htype in {"intern", "contract", "contractor"}:
        base = _plan_intern_or_contract()
    else:
        base = _plan_fulltime_standard(is_lead=flags["lead"])

    # Add cross-functional quality extras
    plan = base + _extras_common()
    return _dedup(plan)
