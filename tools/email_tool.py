# tools/email_tool.py  — professional kickoff email (Python 3.9–safe)
from typing import List, Dict, Optional

def kickoff_email(roles: List[Dict], budget: Optional[str], timeline: Optional[str]) -> str:
    roles_str = ", ".join([r.get("title", "") for r in roles]) or "the role"
    b = budget or "TBD"
    t = timeline or "TBD"

    return f"""Subject: Hiring Kickoff – {roles_str}

Dear Team,

We are initiating the recruitment process for {roles_str}. Please find the initial parameters below:
• Budget: {b}
• Timeline: {t}

Next steps:
1) Finalize role requirements and interview rubric.
2) Publish the approved job description and start sourcing.
3) Schedule structured technical screens and panel interviews.
4) Calibrate the offer package and align on decision timelines.

Your collaboration will be essential to ensure a smooth and timely hire. 
Thank you in advance for your support.

Best regards,
HR Team
"""
