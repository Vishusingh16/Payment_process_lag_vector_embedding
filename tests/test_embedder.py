from src.rag.embedder import get_embedding, get_embeddings


def test_single_embedding_dimension():
    vec = get_embedding("UPI payment failed")
    assert isinstance(vec, list)
    assert len(vec) == 384


def test_embedding_is_floats():
    vec = get_embedding("card declined")
    assert all(isinstance(v, float) for v in vec)


def test_batch_embeddings():
    texts = ["refund policy", "chargeback dispute", "UPI timeout"]
    vecs = get_embeddings(texts)
    assert len(vecs) == 3
    assert all(len(v) == 384 for v in vecs)


def test_different_texts_produce_different_vectors():
    v1 = get_embedding("UPI payment failed")
    v2 = get_embedding("chargeback initiated")
    assert v1 != v2


def test_same_text_produces_same_vector():
    v1 = get_embedding("refund status")
    v2 = get_embedding("refund status")
    assert v1 == v2
