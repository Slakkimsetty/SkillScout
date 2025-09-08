def draft_email(roles, timeline, budget):
    return f"""
Subject: Hiring Plan Kickoff

Hi Team,

We are planning to hire for:
{', '.join([r.title for r in roles])}

Timeline: {timeline or "TBD"}
Budget: {budget or "TBD"}

Next Steps:
1. Finalize Job Descriptions
2. Begin Sourcing
3. Schedule Interviews

Thanks,
HR Agent
"""
