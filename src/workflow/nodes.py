
from typing import Literal, Optional

from pydantic import BaseModel, Field

from langgraph.types import interrupt

from src.llm import llm
from src.state import SupportState
from src.agents.support_agent import run_support_agent
from src.tools.refund_tools import check_eligibility, process_refund


class RequestAnalysis(BaseModel):

    intent: Literal[
        "refund",
        "customer_info",
        "order_status",
        "return_policy",
        "general"
    ]

    order_id: Optional[str] = None
    customer_id: Optional[str] = None

    reason: str = Field(
        description="Short explanation of the customer's request."
    )


def classify_request(state: SupportState):

    classifier = llm.with_structured_output(RequestAnalysis)

    result = classifier.invoke(
        f"""
        Analyze this customer support request.

        Extract the intent and any customer ID or order ID.

        Customer request: {state['message']}
        """
    )

    return {
        "intent": result.intent,
        "order_id": result.order_id or "",
        "customer_id": result.customer_id or ""
    }


def support_node(state: SupportState):

    response = run_support_agent(state["message"])

    return {"response": response}


def refund_check_node(state: SupportState):

    order_id = state.get("order_id", "")

    result = check_eligibility(order_id)

    return {"eligibility": result}


def human_review_node(state: SupportState):

    eligibility = state["eligibility"]

    decision = interrupt({
        "message": "Human approval required for this refund.",
        "order_id": state["order_id"],
        "eligibility": eligibility
    })

    approved = str(decision).lower() == "approve"

    return {"approved": approved}


def process_refund_node(state: SupportState):

    result = process_refund(state["order_id"])

    return {"response": result}


def reject_refund_node(state: SupportState):

    return {
        "response": (
            f"Refund request for {state['order_id']} "
            "was rejected by the human reviewer. "
            "No refund was processed."
        )
    }


def ineligible_node(state: SupportState):

    reason = state["eligibility"]["reason"]

    return {
        "response": f"Your refund request cannot be approved: {reason}"
    }
