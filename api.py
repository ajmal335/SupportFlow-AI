
import os
import uuid
import secrets
from typing import Literal

from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel, Field

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command

from src.workflow.graph import build_graph
from src.config import CHECKPOINT_DIR

from dotenv import load_dotenv

load_dotenv()

ADMIN_API_TOKEN = os.getenv("ADMIN_API_TOKEN")


app = FastAPI(
    title="SupportFlow AI API",
    description="AI-powered customer support API with human refund approval.",
    version="1.0.0"
)


# -------------------------------
# Request Models
# -------------------------------

class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        description="Customer's support message"
    )


class ApprovalRequest(BaseModel):
    decision: Literal["approve", "reject"]


# -------------------------------
# Helper Function
# -------------------------------

def get_graph(checkpointer):
    return build_graph(checkpointer)


# -------------------------------
# Admin Authentication
# -------------------------------

def verify_admin_token(
    x_admin_token: str | None = Header(default=None)
):
    if not ADMIN_API_TOKEN:
        raise HTTPException(
            status_code=503,
            detail="Admin approval is not configured."
        )

    if not x_admin_token or not secrets.compare_digest(
        x_admin_token,
        ADMIN_API_TOKEN
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing admin token."
        )

    return True


# -------------------------------
# Root Endpoint
# -------------------------------

@app.get("/")
def home():
    return {
        "application": "SupportFlow AI",
        "status": "running",
        "version": "1.0.0"
    }


# -------------------------------
# Health Endpoint
# -------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "SupportFlow AI"
    }


# -------------------------------
# Chat Endpoint
# -------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    thread_id = str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    os.makedirs(CHECKPOINT_DIR, exist_ok=True)

    db_path = os.path.join(
        CHECKPOINT_DIR,
        "supportflow.db"
    )

    try:
        with SqliteSaver.from_conn_string(db_path) as checkpointer:

            checkpointer.setup()

            graph = get_graph(checkpointer)

            result = graph.invoke(
                {"message": request.message},
                config=config
            )

            # Check whether human approval is required
            if result.get("__interrupt__"):

                review = result["__interrupt__"][0].value

                return {
                    "status": "pending_approval",
                    "thread_id": thread_id,
                    "review": review,
                    "message": "Refund request is waiting for human approval."
                }

            return {
                "status": "completed",
                "thread_id": thread_id,
                "response": result.get(
                    "response",
                    "No response generated."
                )
            }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Application error: {str(error)}"
        )


# -------------------------------
# Refund Approval Endpoint
# -------------------------------


@app.post("/approve/{thread_id}")
def approve_refund(
    thread_id: str,
    request: ApprovalRequest,
    authorized: bool = Depends(verify_admin_token)
):
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    db_path = os.path.join(
        CHECKPOINT_DIR,
        "supportflow.db"
    )

    try:
        with SqliteSaver.from_conn_string(db_path) as checkpointer:

            checkpointer.setup()

            graph = get_graph(checkpointer)

            # Retrieve the saved workflow state
            snapshot = graph.get_state(config)

            # Verify that the workflow thread exists
            if not snapshot.config:
                raise HTTPException(
                    status_code=404,
                    detail="Workflow thread not found."
                )

            # Check for pending human approval
            has_pending_interrupt = any(
                task.interrupts
                for task in snapshot.tasks
            )

            if not has_pending_interrupt:
                raise HTTPException(
                    status_code=400,
                    detail="This workflow is not waiting for approval."
                )

            # Resume the interrupted workflow
            result = graph.invoke(
                Command(resume=request.decision),
                config=config
            )

            return {
                "status": "completed",
                "thread_id": thread_id,
                "decision": request.decision,
                "response": result.get(
                    "response",
                    "No response generated."
                )
            }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Application error: {str(error)}"
        )
