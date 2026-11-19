
from langgraph.graph import StateGraph, START, END

from langgraph.checkpoint.sqlite import SqliteSaver

from src.state import SupportState

from src.workflow.nodes import (
    classify_request,
    support_node,
    refund_check_node,
    human_review_node,
    process_refund_node,
    reject_refund_node,
    ineligible_node
)

from src.workflow.routing import (
    route_intent,
    route_eligibility,
    route_approval
)


def build_graph(checkpointer):

    builder = StateGraph(SupportState)

    builder.add_node("classify", classify_request)
    builder.add_node("support", support_node)
    builder.add_node("refund_check", refund_check_node)
    builder.add_node("human_review", human_review_node)
    builder.add_node("process_refund", process_refund_node)
    builder.add_node("reject_refund", reject_refund_node)
    builder.add_node("ineligible", ineligible_node)

    builder.add_edge(START, "classify")

    builder.add_conditional_edges(
        "classify",
        route_intent,
        {
            "support": "support",
            "refund_check": "refund_check"
        }
    )

    builder.add_edge("support", END)

    builder.add_conditional_edges(
        "refund_check",
        route_eligibility,
        {
            "human_review": "human_review",
            "ineligible": "ineligible"
        }
    )

    builder.add_conditional_edges(
        "human_review",
        route_approval,
        {
            "process_refund": "process_refund",
            "reject_refund": "reject_refund"
        }
    )

    builder.add_edge("process_refund", END)
    builder.add_edge("reject_refund", END)
    builder.add_edge("ineligible", END)

    return builder.compile(checkpointer=checkpointer)
