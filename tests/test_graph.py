from state import AgentState
from graph import build_graph

def test_graph_runs():
    g = build_graph()
    state = AgentState(session_id="t1", user_query="I need a founding engineer and a GenAI intern")
    out = g.invoke(state.model_dump())
    assert "artifacts" in out
