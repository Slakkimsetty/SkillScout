def build_checklist(slots):
    """Return a structured hiring checklist as dict."""
    stages = [
        {"stage": "Intake", "owner": "HR", "exit": "JD approved"},
        {"stage": "Sourcing", "owner": "Recruiter", "exit": "10 candidates"},
        {"stage": "Screening", "owner": "HR", "exit": "Shortlist ready"},
        {"stage": "Technical", "owner": "Engineering", "exit": "Tech evaluation"},
        {"stage": "Culture Fit", "owner": "Founder", "exit": "Culture approval"},
        {"stage": "Offer", "owner": "HR", "exit": "Offer accepted"},
        {"stage": "Onboarding", "owner": "Manager", "exit": "Hired onboarded"},
    ]
    return stages
