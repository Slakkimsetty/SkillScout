# app.py — interactive clarifying step + results
import uuid, json
from typing import List
import streamlit as st
from state import AgentState
from graph import build_graph

st.set_page_config(page_title="SkillScout – HR Agent", page_icon="🧭", layout="wide")

# Hide default chrome for a cleaner look
st.markdown("""
<style>
header {visibility:hidden;} [data-testid="stToolbar"]{visibility:hidden;} footer{visibility:hidden;}
.block-container{max-width:1120px; padding-top:.6rem;}
.card{ background:var(--card,#11182714); border:1px solid rgba(125,125,125,.2);
       border-radius:14px; padding:14px 16px; }
</style>
""", unsafe_allow_html=True)

# ---------------- Session ----------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "last" not in st.session_state:
    st.session_state.last = None  # AgentState after each run

# ---------------- Helpers ----------------
def missing_slots(state: AgentState):
    """Return dict of which fields are missing."""
    s = state.slots
    return {
        "budget": not bool(s.budget),
        "timeline": not bool(s.timeline),
        "location": not bool(s.location),
        "hiring_type": not bool(s.hiring_type),
        "skills": not bool(s.skills_hint),
    }

def run_graph_with(state: AgentState) -> AgentState:
    app = build_graph()
    out = app.invoke(state.model_dump())
    return AgentState.model_validate(out)

# ---------------- HERO ----------------
st.markdown("## What roles do you need?")
st.caption("Describe your hiring request. I’ll ask what’s missing, then draft JDs and a hiring plan.")

prompt = st.text_input(
    " ",
    value="i need to hire an ai engineer. can you help?",
    label_visibility="collapsed",
    placeholder="e.g., need a founding engineer and a GenAI intern (remote, 8 weeks, $150–180k)"
)

if st.button("Ask Agent", type="primary"):
    # First pass: run the graph with just the raw prompt
    first = AgentState(session_id=st.session_state.session_id, user_query=prompt.strip())
    st.session_state.last = run_graph_with(first)

st.divider()

# ================= FLOW =================
if not st.session_state.last:
    st.info("Enter a request above and click **Ask Agent**.")
else:
    state = st.session_state.last
    miss = missing_slots(state)

    # ------ STEP 1: Clarify (only when something is missing) ------
    if any(miss.values()):
        st.subheader("Clarify a few details")
        st.caption("Answer only what’s missing; you can leave others blank.")

        with st.form("clarify_form", clear_on_submit=False):
            c1, c2 = st.columns(2)

            # budget
            budget_val = None
            if miss["budget"]:
                with c1:
                    budget_val = st.text_input("Budget (e.g., $150k, $40/hr, 12 LPA)")

            # timeline
            timeline_val = None
            if miss["timeline"]:
                with c2:
                    timeline_val = st.text_input("Timeline (e.g., 6 weeks, next 2 months)")

            # location
            location_val = None
            if miss["location"]:
                with c1:
                    location_val = st.selectbox(
                        "Location", ["", "Remote", "Hybrid", "Onsite"], index=0
                    )

            # hiring type
            type_val = None
            if miss["hiring_type"]:
                with c2:
                    type_val = st.selectbox(
                        "Hiring type", ["", "Full-time", "Contract", "Intern"], index=0
                    )

            # skills
            skills_val = None
            if miss["skills"]:
                with c1:
                    skills_val = st.text_input("Key skills (comma-separated) e.g., python, kubernetes")

            submitted = st.form_submit_button("Continue")
            if submitted:
                # Update the existing state slots with provided answers
                s = state.slots
                if miss["budget"] and budget_val:
                    s.budget = budget_val.strip()
                if miss["timeline"] and timeline_val:
                    s.timeline = timeline_val.strip()
                if miss["location"] and location_val:
                    s.location = location_val.strip() or None
                if miss["hiring_type"] and type_val:
                    s.hiring_type = type_val.strip() or None
                if miss["skills"] and skills_val:
                    parsed = [x.strip() for x in skills_val.split(",") if x.strip()]
                    # avoid duplicates
                    existing = set(s.skills_hint or [])
                    s.skills_hint = list(existing.union(parsed))

                # Re-run the graph with updated slots (same user_query/session_id)
                st.session_state.last = run_graph_with(state)
                st.rerun()

    # ------ STEP 2: Results ------
    state = st.session_state.last
    tabs = st.tabs(["Job Descriptions", "Checklist", "Export", "Analytics"])

    with tabs[0]:
        if not state.artifacts.jds:
            st.info("Fill the clarifying details and click **Continue** to get JDs.")
        else:
            for title, md in state.artifacts.jds.items():
                with st.container(border=True):
                    st.markdown(f"**{title} (Draft)**")
                    st.markdown(md)
                    st.download_button("Download JD (Markdown)", data=md,
                                       file_name=f"{title.replace(' ','_').lower()}_jd.md")

    with tabs[1]:
        if not state.artifacts.plan_json:
            st.info("No plan yet. Fill clarifications and continue.")
        else:
            st.markdown(state.artifacts.plan_markdown)
            st.json(state.artifacts.plan_json)

    with tabs[2]:
        payload = state.model_dump()
        st.download_button("Download session.json", data=json.dumps(payload, indent=2),
                           file_name="session.json")
        st.download_button("Download results.md", data=state.artifacts.summary_md,
                           file_name="results.md")

    with tabs[3]:
        a = state.analytics or {}
        c1, c2, c3 = st.columns(3)
        c1.metric("Roles Created", a.get("roles_created", 0))
        c2.metric("Checklist Items", a.get("checklist_items", 0))
        c3.metric("Sessions", a.get("sessions", 1))
