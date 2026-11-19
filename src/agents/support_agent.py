
from langchain_core.messages import HumanMessage, ToolMessage

from src.llm import llm

from src.tools.order_tools import (
    get_customer_details,
    get_order_status
)

from src.tools.policy_tools import get_return_policy


TOOLS = [
    get_customer_details,
    get_order_status,
    get_return_policy
]

TOOL_MAP = {tool.name: tool for tool in TOOLS}

llm_with_tools = llm.bind_tools(TOOLS)


def run_support_agent(user_message: str) -> str:

    messages = [
        HumanMessage(content=user_message)
    ]

    for _ in range(5):

        response = llm_with_tools.invoke(messages)

        if not response.tool_calls:
            return response.text

        messages.append(response)

        for tool_call in response.tool_calls:

            tool = TOOL_MAP.get(tool_call["name"])

            if not tool:
                result = "Requested tool is unavailable."
            else:
                try:
                    result = tool.invoke(tool_call["args"])
                except Exception:
                    result = "The requested operation could not be completed."

            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"]
                )
            )

    return "I could not complete your request. Please contact support."
