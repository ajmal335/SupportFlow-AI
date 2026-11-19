
import uuid

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command

from src.workflow.graph import build_graph
from src.config import CHECKPOINT_DIR


def main():

    print("\n===================================")
    print("       SUPPORTFLOW AI")
    print("    AI Customer Support Agent")
    print("===================================\n")

    user_message = input("Customer: ").strip()

    if not user_message:
        print("Please enter a message.")
        return

    thread_id = str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    db_path = f"{CHECKPOINT_DIR}/supportflow.db"

    with SqliteSaver.from_conn_string(db_path) as checkpointer:

        graph = build_graph(checkpointer)

        print("\nProcessing your request...\n")

        result = graph.invoke(
            {"message": user_message},
            config=config
        )

        if result.get("__interrupt__"):

            review = result["__interrupt__"][0].value

            print("\n========== HUMAN REVIEW ==========")
            print("Order ID:", review["order_id"])
            print("Eligibility:", review["eligibility"])
            print("\nRefund amount: PKR",
                  review["eligibility"]["refund_amount"])

            decision = input(
                "\nApprove or reject this refund? "
            ).strip().lower()

            while decision not in ("approve", "reject"):
                decision = input(
                    "Enter approve or reject: "
                ).strip().lower()

            result = graph.invoke(
                Command(resume=decision),
                config=config
            )

        print("\n========== FINAL RESPONSE ==========")
        print(result.get("response", "No response generated."))


if __name__ == "__main__":
    main()
