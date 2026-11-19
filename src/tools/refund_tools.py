
from datetime import date

from langchain.tools import tool

from src.data_loader import load_orders, save_json


def check_eligibility(order_id: str) -> dict:

    orders = load_orders()

    order = next(
        (item for item in orders if item["order_id"] == order_id),
        None
    )

    if not order:
        return {"eligible": False, "reason": "Order not found."}

    if order["status"] != "Delivered":
        return {
            "eligible": False,
            "reason": "Order has not been delivered."
        }

    if order["refund_status"] != "None":
        return {
            "eligible": False,
            "reason": "A refund request has already been processed or submitted."
        }

    if order["product_condition"] != "Unused and original packaging":
        return {
            "eligible": False,
            "reason": "Product condition does not meet return requirements."
        }

    delivery_date = date.fromisoformat(order["delivery_date"])
    days_since_delivery = (date.today() - delivery_date).days

    if days_since_delivery < 0 or days_since_delivery > 30:
        return {
            "eligible": False,
            "reason": "The 30-day return period has expired or delivery date is invalid."
        }

    return {
        "eligible": True,
        "reason": "Order meets the configured return eligibility requirements.",
        "order_id": order_id,
        "product": order["product"],
        "refund_amount": order["price"]
    }


@tool
def check_refund_eligibility(order_id: str) -> str:
    """Check whether an order qualifies for a refund."""

    return str(check_eligibility(order_id))


def process_refund(order_id: str) -> str:
    """Update the sample database after human approval."""

    orders = load_orders()

    for order in orders:

        if order["order_id"] == order_id:

            if order["refund_status"] != "None":
                return "Refund request has already been submitted or processed."

            order["refund_status"] = "Approved - Simulated"
            order["return_requested"] = True

            save_json("orders.json", orders)

            return (
                f"Refund approved successfully for {order_id}. "
                f"Amount: PKR {order['price']}. "
                "This is a simulated transaction."
            )

    return "Order not found."
