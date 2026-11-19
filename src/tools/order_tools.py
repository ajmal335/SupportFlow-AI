
from langchain.tools import tool

from src.data_loader import load_customers, load_orders


@tool
def get_customer_details(customer_id: str) -> str:
    """Find customer information using customer ID."""

    for customer in load_customers():
        if customer["customer_id"] == customer_id:
            return str(customer)

    return f"Customer {customer_id} not found."


@tool
def get_order_status(order_id: str) -> str:
    """Find order details and delivery status using order ID."""

    for order in load_orders():
        if order["order_id"] == order_id:
            return str(order)

    return f"Order {order_id} not found."
