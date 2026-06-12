"""
Mock tools that simulate real Razorpay backend calls.
In production these would be actual API calls to the payment gateway.
"""

import random

MOCK_TRANSACTIONS = {
    "TXN001": {"status": "failed", "reason": "Bank server unavailable", "amount": 1500, "method": "UPI"},
    "TXN002": {"status": "success", "reason": None, "amount": 2999, "method": "Card"},
    "TXN003": {"status": "refunded", "reason": "Duplicate payment", "amount": 500, "method": "Net Banking"},
    "TXN004": {"status": "pending", "reason": "Awaiting bank confirmation", "amount": 750, "method": "UPI"},
    "TXN005": {"status": "failed", "reason": "Insufficient balance", "amount": 3200, "method": "Card"},
    "TXN006": {"status": "success", "reason": None, "amount": 199, "method": "Wallet"},
    "TXN007": {"status": "failed", "reason": "Card authentication failed", "amount": 4500, "method": "Card"},
    "TXN008": {"status": "refunded", "reason": "Customer requested refund", "amount": 999, "method": "UPI"},
}


def get_transaction_status(transaction_id: str) -> dict:
    """
    Mock tool: checks the status of a payment transaction.
    Returns status, failure reason (if any), amount, and payment method.
    """
    txn = MOCK_TRANSACTIONS.get(transaction_id.upper())
    if not txn:
        return {
            "found": False,
            "transaction_id": transaction_id,
            "message": "Transaction not found. Please verify the transaction ID.",
        }
    return {
        "found": True,
        "transaction_id": transaction_id.upper(),
        "status": txn["status"],
        "reason": txn["reason"],
        "amount": txn["amount"],
        "method": txn["method"],
    }


def check_refund_status(transaction_id: str) -> dict:
    """
    Mock tool: checks if a refund has been initiated for a transaction.
    """
    txn = MOCK_TRANSACTIONS.get(transaction_id.upper())
    if not txn:
        return {"found": False, "message": "Transaction not found."}

    if txn["status"] == "refunded":
        return {
            "found": True,
            "transaction_id": transaction_id.upper(),
            "refund_status": "completed",
            "message": f"Refund of ₹{txn['amount']} has been processed.",
        }
    elif txn["status"] == "failed":
        return {
            "found": True,
            "transaction_id": transaction_id.upper(),
            "refund_status": "auto-initiated",
            "message": f"Auto-refund of ₹{txn['amount']} initiated. Expect credit in 5-7 business days.",
        }
    else:
        return {
            "found": True,
            "transaction_id": transaction_id.upper(),
            "refund_status": "not_applicable",
            "message": f"Transaction status is '{txn['status']}'. No refund applicable.",
        }


AVAILABLE_TOOLS = {
    "get_transaction_status": {
        "fn": get_transaction_status,
        "description": "Check the status of a payment transaction by transaction ID",
        "trigger_keywords": ["transaction", "txn", "TXN", "status", "check payment"],
    },
    "check_refund_status": {
        "fn": check_refund_status,
        "description": "Check the refund status for a transaction",
        "trigger_keywords": ["refund", "money back", "reversal", "credited back"],
    },
}
