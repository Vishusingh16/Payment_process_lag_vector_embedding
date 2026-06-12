from src.tools import get_transaction_status, check_refund_status


def test_known_transaction_found():
    result = get_transaction_status("TXN001")
    assert result["found"] is True
    assert result["transaction_id"] == "TXN001"
    assert result["status"] == "failed"


def test_transaction_case_insensitive():
    result = get_transaction_status("txn001")
    assert result["found"] is True
    assert result["transaction_id"] == "TXN001"


def test_unknown_transaction():
    result = get_transaction_status("TXN999")
    assert result["found"] is False
    assert "not found" in result["message"].lower()


def test_failed_transaction_has_reason():
    result = get_transaction_status("TXN001")
    assert result["reason"] is not None


def test_success_transaction_no_reason():
    result = get_transaction_status("TXN002")
    assert result["status"] == "success"
    assert result["reason"] is None


def test_refund_status_refunded():
    result = check_refund_status("TXN003")
    assert result["found"] is True
    assert result["refund_status"] == "completed"


def test_refund_status_failed_transaction():
    result = check_refund_status("TXN001")
    assert result["refund_status"] == "auto-initiated"


def test_refund_status_unknown():
    result = check_refund_status("TXN999")
    assert result["found"] is False
