from fastapi import FastAPI
from pydantic import BaseModel
from src.agent import run_agent
from src.tools import get_transaction_status, check_refund_status

app = FastAPI(
    title="Payment Support RAG Agent",
    description="Razorpay-style support agent powered by RAG + tool use",
    version="1.0.0",
)


class QuestionRequest(BaseModel):
    question: str


class TransactionRequest(BaseModel):
    transaction_id: str


@app.get("/health")
def health():
    return {"status": "ok", "service": "payment-support-rag-agent"}


@app.post("/ask")
def ask(request: QuestionRequest):
    """
    Main endpoint. Accepts a natural language question.
    Agent decides whether to use RAG or tool automatically.
    """
    result = run_agent(request.question)
    return result


@app.get("/transaction/{transaction_id}")
def transaction_status(transaction_id: str):
    """Direct tool endpoint to check a specific transaction."""
    return get_transaction_status(transaction_id)


@app.get("/refund/{transaction_id}")
def refund_status(transaction_id: str):
    """Direct tool endpoint to check refund status."""
    return check_refund_status(transaction_id)
