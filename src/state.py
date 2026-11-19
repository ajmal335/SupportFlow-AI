
from typing import TypedDict


class SupportState(TypedDict, total=False):

    message: str
    intent: str
    customer_id: str
    order_id: str

    eligibility: dict
    approved: bool

    response: str
