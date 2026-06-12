from src.rag.loader import load_and_chunk
from src.rag.embedder import get_embedding, get_embeddings
from src.rag.vector_store import VectorStore

DATA_PATH = "data/support_policies.txt"

# Singleton store — built once at import time
_store: VectorStore | None = None


def _build_store() -> VectorStore:
    chunks = load_and_chunk(DATA_PATH)
    texts = [c["text"] for c in chunks]
    embeddings = get_embeddings(texts)
    store = VectorStore()
    store.add(chunks, embeddings)
    return store


def get_store() -> VectorStore:
    global _store
    if _store is None:
        _store = _build_store()
    return _store


def retrieve(question: str, top_k: int = 3) -> list[dict]:
    store = get_store()
    query_vec = get_embedding(question)
    return store.search(query_vec, top_k=top_k)


def build_prompt(question: str, context_chunks: list[dict]) -> str:
    context_lines = []
    for chunk in context_chunks:
        context_lines.append(
            f"[{chunk['category']}] {chunk['issue']}\n{chunk['text']}"
        )
    context = "\n\n".join(context_lines)

    return f"""You are a Razorpay payment support agent.
Use ONLY the context below to answer the customer's question.
If the answer is not in the context, respond with: "I don't have specific information on this. Please contact Razorpay support."

--- CONTEXT START ---
{context}
--- CONTEXT END ---

Customer Question: {question}

Answer:"""


def answer_with_rag(question: str, top_k: int = 3) -> dict:
    """
    Full RAG pipeline: retrieve relevant chunks, build prompt, return structured result.
    Since we are running without an LLM API, we return the best matching policy
    as the answer. In production you would pass the prompt to an LLM.
    """
    chunks = retrieve(question, top_k=top_k)
    prompt = build_prompt(question, chunks)

    # --- Mock LLM: return the most relevant chunk as the answer ---
    # In production: replace this block with an actual LLM call
    # e.g. response = anthropic_client.messages.create(...)
    if chunks:
        best = chunks[0]
        # Extract just the Resolution section if present
        import re
        resolution_match = re.search(r"Resolution:\s*(.+?)(?=\w+:|$)", best["text"])
        if resolution_match:
            answer = resolution_match.group(1).strip()
        else:
            answer = best["text"]
    else:
        answer = "I don't have specific information on this. Please contact Razorpay support."

    return {
        "question": question,
        "answer": answer,
        "sources": [
            {"category": c["category"], "issue": c["issue"], "score": c.get("score", 0)}
            for c in chunks
        ],
        "prompt": prompt,
    }
