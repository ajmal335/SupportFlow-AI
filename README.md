
# SupportFlow AI

An AI-powered customer support agent built using LangChain,
LangGraph, Gemini API, and SQLite.

## Features

- Customer information lookup
- Order status checking
- Return and refund policy retrieval
- Refund eligibility validation
- Human-in-the-Loop refund approval
- SQLite workflow persistence
- Natural language customer responses

## Technology Stack

- Python
- LangChain
- LangGraph
- Google Gemini API
- Pydantic
- SQLite

## Architecture

Customer Request
       |
       v
Request Classification
       |
       +---- General Support
       |         |
       |         v
       |    LangChain Agent
       |         |
       |         v
       |    Customer Response
       |
       +---- Refund Request
                 |
                 v
          Eligibility Check
                 |
                 v
          Human Approval
                 |
            +----+----+
            |         |
          Approve   Reject
            |         |
            v         v
        Process    Reject
        Refund     Request

## Installation

Clone the repository:

    git clone YOUR_REPOSITORY_URL

Navigate into the project:

    cd SupportFlow_AI

Install dependencies:

    pip install -r requirements.txt

Create a .env file:

    GEMINI_API_KEY=your_api_key

Run the application:

    python main.py

## Important

Refund processing is simulated using sample JSON data.
No real payments are initiated.
