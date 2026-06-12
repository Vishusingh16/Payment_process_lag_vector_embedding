"""
Agent layer: decides whether to use a tool or RAG based on the user query.

Decision logic:
  1. If query contains a transaction ID (TXNxxx pattern) → call tool first, then augment with RAG
  2. If query has refund-check keywords + transaction ID → call refund tool
  3. Otherwise → pure RAG answer
"""

import re
from src.rag.rag_pipeline import answer_with_rag
from src.tools import get_transaction_status, check_refund_status

TXN_PATTERN = re.compile(r"\bTXN\d+\b", re.IGNORECASE)


def _extract_txn_id(text: str) -> str | None:
    match = TXN_PATTERN.search(text)
    return match.group(0).upper() if match else None


def _is_refund_query(text: str) -> bool:
    keywords = ["refund", "money back", "credited", "reversal", "returned"]
    return any(kw in text.lower() for kw in keywords)


def run_agent(question: str) -> dict:
    """
    Main agent entrypoint. Routes question to tool or RAG.
    Returns a unified response dict.
    """
    txn_id = _extract_txn_id(question)

    # --- Tool path ---
    if txn_id:
        if _is_refund_query(question):
            tool_result = check_refund_status(txn_id)
            tool_used = "check_refund_status"
        else:
            tool_result = get_transaction_status(txn_id)
            tool_used = "get_transaction_status"

        # Use RAG to enrich the answer with policy context
        rag_result = answer_with_rag(question, top_k=2)

        if tool_result.get("found"):
            if tool_used == "get_transaction_status":
                tool_answer = (
                    f"Transaction {txn_id}: Status is '{tool_result['status']}' "
                    f"via {tool_result['method']} for ₹{tool_result['amount']}."
                )
                if tool_result.get("reason"):
                    tool_answer += f" Reason: {tool_result['reason']}."
            else:
                tool_answer = tool_result["message"]
        else:
            tool_answer = tool_result.get("message", "Transaction not found.")

        final_answer = f"{tool_answer}\n\nPolicy context: {rag_result['answer']}"

        return {
            "question": question,
            "mode": "tool+rag",
            "tool_used": tool_used,
            "tool_result": tool_result,
            "answer": final_answer,
            "sources": rag_result["sources"],
        }

    # --- Pure RAG path ---
    rag_result = answer_with_rag(question, top_k=3)
    return {
        "question": question,
        "mode": "rag",
        "tool_used": None,
        "tool_result": None,
        "answer": rag_result["answer"],
        "sources": rag_result["sources"],
    }
