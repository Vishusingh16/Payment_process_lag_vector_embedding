from src.rag.loader import load_and_chunk


def test_loader_returns_chunks():
    chunks = load_and_chunk("data/support_policies.txt")
    assert len(chunks) > 0


def test_chunks_have_required_fields():
    chunks = load_and_chunk("data/support_policies.txt")
    for chunk in chunks:
        assert "id" in chunk
        assert "category" in chunk
        assert "issue" in chunk
        assert "text" in chunk


def test_categories_are_known():
    chunks = load_and_chunk("data/support_policies.txt")
    known = {"PAYMENT_FAILURE", "REFUND", "DISPUTE"}
    categories = {c["category"] for c in chunks}
    assert categories.issubset(known | {"UNKNOWN"})


def test_chunks_have_non_empty_text():
    chunks = load_and_chunk("data/support_policies.txt")
    assert all(len(c["text"]) > 10 for c in chunks)
