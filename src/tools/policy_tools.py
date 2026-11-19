
from langchain.tools import tool

from src.data_loader import load_policies


@tool
def get_return_policy() -> str:
    """Retrieve return and refund policy information."""

    return load_policies()
