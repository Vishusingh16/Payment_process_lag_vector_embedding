from src.rag.vector_store import VectorStore
from src.rag.embedder import get_embedding, get_embeddings


def _build_store():
    chunks = [
        {"id": 0, "category": "PAYMENT_FAILURE", "issue": "UPI Timeout", "text": "UPI payment failed due to bank timeout"},
        {"id": 1, "category": "REFUND", "issue": "Refund Processing", "text": "Refunds take 5-7 business days"},
        {"id": 2, "category": "DISPUTE", "issue": "Chargeback", "text": "Chargeback is raised by the card network"},
    ]
    embeddings = get_embeddings([c["text"] for c in chunks])
    store = VectorStore()
    store.add(chunks, embeddings)
    return store


def test_store_length():
    store = _build_store()
    assert len(store) == 3


def test_search_returns_top_k():
    store = _build_store()
    results = store.search(get_embedding("UPI payment failed"), top_k=2)
    assert len(results) == 2


def test_search_most_relevant_first():
    store = _build_store()
    results = store.search(get_embedding("UPI timeout bank"), top_k=3)
    # The UPI chunk should be most similar (lowest L2 distance = lowest score)
    assert results[0]["issue"] == "UPI Timeout"


def test_search_results_have_score():
    store = _build_store()
    results = store.search(get_embedding("refund"), top_k=1)
    assert "score" in results[0]
    assert isinstance(results[0]["score"], float)
