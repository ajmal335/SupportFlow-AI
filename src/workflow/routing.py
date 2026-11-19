
def route_intent(state):

    if state["intent"] == "refund":
        return "refund_check"

    return "support"


def route_eligibility(state):

    if state["eligibility"]["eligible"]:
        return "human_review"

    return "ineligible"


def route_approval(state):

    if state["approved"]:
        return "process_refund"

    return "reject_refund"
