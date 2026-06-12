from src.agent import run_agent


def test_pure_rag_query():
    result = run_agent("How long does a refund take?")
    assert result["mode"] == "rag"
    assert result["tool_used"] is None
    assert len(result["answer"]) > 10
    assert len(result["sources"]) > 0


def test_tool_query_with_txn_id():
    result = run_agent("Check transaction TXN001")
    assert result["mode"] == "tool+rag"
    assert result["tool_used"] == "get_transaction_status"
    assert "TXN001" in result["answer"]


def test_refund_query_with_txn_id():
    result = run_agent("What is the refund status for TXN003?")
    assert result["mode"] == "tool+rag"
    assert result["tool_used"] == "check_refund_status"


def test_upi_failure_query():
    result = run_agent("My UPI payment failed but money was deducted")
    assert result["mode"] == "rag"
    assert len(result["sources"]) > 0
    # Should surface PAYMENT_FAILURE category
    categories = [s["category"] for s in result["sources"]]
    assert "PAYMENT_FAILURE" in categories


def test_unknown_transaction_handled_gracefully():
    result = run_agent("Check transaction TXN999")
    assert "not found" in result["answer"].lower() or "TXN999" in result["answer"]


def test_dispute_query():
    result = run_agent("What is the chargeback process?")
    assert result["mode"] == "rag"
    categories = [s["category"] for s in result["sources"]]
    assert "DISPUTE" in categories


def test_card_declined_query():
    result = run_agent("My card payment was declined")
    assert result["mode"] == "rag"
    assert len(result["answer"]) > 10


def test_answer_is_string():
    result = run_agent("How do I raise a dispute?")
    assert isinstance(result["answer"], str)
