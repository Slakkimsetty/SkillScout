import uuid
import json
import streamlit as st
from state import AgentState
from graph import build_graph

# ---------- Page Setup ----------
st.set_page_config(
    page_title="HR Agent",
    page_icon="🤝",
    layout="wide"
)

# Subtle CSS polish
st.markdown("""
<style>
/* Card-like containers */
.block-container {
  padding-top: 2rem;
}
div[data-testid="stMarkdownContainer"] h2, 
div[data-testid="stMarkdownContainer"] h3, 
div[data-testid="stMarkdownContainer"] h4 {
  margin-top: 0.6rem;
}
/* Buttons */
.stButton>button {
  border-radius: 12px;
  padding: 0.6rem 1rem;
  font-weight: 600;
}
/* Inputs */
textarea, input[type="text"] {
  border-radius: 10px !important;
}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------- Session State ----------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "history" not in st.session_state:
    st.session_state.history = []  # list of (prompt, artifacts_dict)

# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ Controls")
    st.caption("Session & utilities")
    st.code(st.session_state.session_id, language="text")

    colA, colB = st.columns(2)
    with colA:
        if st.button("🔁 New Session", use_container_width=True):
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.history = []
            st.experimental_rerun()
    with colB:
        if st.button("🧹 Clear History", type="secondary", use_container_width=True):
            st.session_state.history = []
            st.experimental_rerun()

    st.markdown("---")
    st.caption("Tip: You can export Markdown/JSON from the tabs below after running the agent.")

# ---------- Header ----------
st.title("🤝 HR Agentic App")
st.write("Plan startup hiring: clarifications → Job Descriptions → Plan → Email.")

# ---------- Prompt ----------
default_text = "I need to hire a founding engineer and a GenAI intern."
user_input = st.text_area(
    "Enter your hiring request:",
    value=default_text,
    height=90,
    placeholder="Describe the roles, budget, timeline, and location if you have them…"
)

run = st.button("▶️ Run Agent", type="primary")

# ---------- Run the agent ----------
artifacts_to_show = None
if run and user_input.strip():
    state = AgentState(session_id=st.session_state.session_id, user_query=user_input.strip())
    app = build_graph()
    out = app.invoke(state.model_dump())
    state = AgentState.model_validate(out)

    # Save only artifacts to history (keeps memory light)
    st.session_state.history.append({
        "prompt": user_input.strip(),
        "artifacts": state.artifacts.model_dump()
    })
    artifacts_to_show = state.artifacts.model_dump()
elif st.session_state.history:
    # Show the newest run by default
    artifacts_to_show = st.session_state.history[-1]["artifacts"]

# ---------- Nothing to show yet ----------
if not artifacts_to_show:
    st.info("Enter a request and click **Run Agent** to see results.")
    st.stop()

# ---------- Helpers ----------
def build_combined_markdown(a: dict) -> str:
    md = []
    md.append("## Hiring Assistant Results")
    if a.get("result_markdown"):
        md.append(a["result_markdown"])
    else:
        # Rebuild a pretty overview if presenter_markdown isn't set
        if a.get("jds"):
            md.append("### Job Descriptions")
            for title, jd in a["jds"].items():
                md.append(jd)
        if a.get("plan_markdown"):
            md.append("### Hiring Plan")
            md.append(a["plan_markdown"])
        if a.get("email_draft"):
            md.append("### Draft Email\n```\n" + a["email_draft"] + "\n```")
    return "\n\n".join(md)

def build_export_json(a: dict) -> str:
    # make sure JSON is serializable
    return json.dumps(a, indent=2, ensure_ascii=False)

a = artifacts_to_show
combined_md = build_combined_markdown(a)
export_json = build_export_json(a)

# ---------- Tabs ----------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🧭 Overview", "📄 Job Descriptions", "📋 Plan", "✉️ Email", "🧱 Raw JSON"]
)

with tab1:
    st.subheader("Overview")
    st.markdown(combined_md)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "⬇️ Download Markdown",
            data=combined_md,
            file_name="hr_agent_output.md",
            mime="text/markdown",
            use_container_width=True
        )
    with col2:
        st.download_button(
            "⬇️ Download JSON",
            data=export_json,
            file_name="hr_agent_output.json",
            mime="application/json",
            use_container_width=True
        )

with tab2:
    st.subheader("Job Descriptions")
    jds = a.get("jds", {})
    if jds:
        for title, jd in jds.items():
            with st.expander(f"JD — {title}", expanded=True):
                st.markdown(jd)
    else:
        st.info("No JDs generated in this run.")

with tab3:
    st.subheader("Hiring Plan")
    if a.get("plan_markdown"):
        st.markdown(a["plan_markdown"])
    else:
        st.info("No plan found.")
    st.markdown("**Plan (JSON)**")
    st.json(a.get("plan_json", []), expanded=False)

with tab4:
    st.subheader("Draft Email")
    if a.get("email_draft"):
        st.code(a["email_draft"], language="text")
    else:
        st.info("No email draft found.")

with tab5:
    st.subheader("Raw Artifacts JSON")
    st.json(a, expanded=False)

# ---------- History Panel ----------
st.markdown("---")
st.caption("Previous runs")
if not st.session_state.history:
    st.write("(none)")
else:
    for i, h in enumerate(reversed(st.session_state.history), start=1):
        with st.expander(f"Run #{len(st.session_state.history) - i + 1}: {h['prompt'][:60]}…"):
            st.json(h["artifacts"], expanded=False)
