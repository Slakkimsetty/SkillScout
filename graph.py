from langgraph.graph import StateGraph, END
from state import AgentState
from nodes.intake import intake_node
from nodes.clarifier import clarifier_node
from nodes.jd_generator import jd_generator_node
from nodes.plan_builder import plan_builder_node
from nodes.email_writer import email_writer_node
from nodes.presenter import presenter_node

def build_graph():
    g = StateGraph(dict)

    def wrap(func):
        def _f(d):
            return func(AgentState.model_validate(d)).model_dump()
        return _f

    g.add_node("intake", wrap(intake_node))
    g.add_node("clarifier", wrap(clarifier_node))
    g.add_node("jd_generator", wrap(jd_generator_node))
    g.add_node("plan_builder", wrap(plan_builder_node))
    g.add_node("email_writer", wrap(email_writer_node))
    g.add_node("presenter", wrap(presenter_node))

    g.set_entry_point("intake")
    g.add_edge("intake", "clarifier")
    g.add_edge("clarifier", "jd_generator")
    g.add_edge("jd_generator", "plan_builder")
    g.add_edge("plan_builder", "email_writer")
    g.add_edge("email_writer", "presenter")
    g.add_edge("presenter", END)

    return g.compile()
