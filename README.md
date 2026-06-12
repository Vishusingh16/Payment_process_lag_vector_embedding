# Payment Support RAG Agent

A Razorpay-style customer support agent that combines **Retrieval-Augmented Generation (RAG)** with **tool use** to answer payment-related queries. It intelligently routes questions — looking up live transaction data when a transaction ID is present, and falling back to policy documents for general questions.

---

## What It Covers

- **Payment failures** — UPI timeouts, insufficient balance, card auth failures, bank downtime
- **Refunds** — processing timelines, failed refunds, auto-refund logic
- **Disputes & chargebacks** — resolution timelines and process
- **Transaction lookups** — real-time status checks by transaction ID (TXN001–TXN008)
- **General policy queries** — answered via semantic search over support documents

---

## How It Works

```
User Query
    │
    ▼
Does query contain a TXN ID?
   ├─ Yes → Call tool (get_transaction_status or check_refund_status)
   │         + augment with RAG policy context
   └─ No  → Pure RAG answer from support_policies.txt
```

The knowledge base (`data/support_policies.txt`) is embedded using `sentence-transformers` and indexed in a FAISS vector store for fast semantic retrieval.

---

## Project Structure

```
payment-support-rag-agent/
├── main.py                  # CLI entry point
├── requirements.txt
├── data/
│   └── support_policies.txt # Knowledge base (payment policies)
└── src/
    ├── agent/               # Routing logic (tool vs RAG)
    ├── api/                 # FastAPI server
    ├── rag/                 # Embedder, vector store, RAG pipeline
    └── tools/               # Mock transaction & refund tools
```

---

## Setup

**1. Clone and install dependencies**

```bash
git clone <repo-url>
cd payment-support-rag-agent
pip install -r requirements.txt
```

**2. (Optional) Create a `.env` file** if you add API keys later.

---

## Running the Project

### Interactive CLI

```bash
python main.py
```

Ask questions like:
- `My UPI payment failed but money was deducted. What should I do?`
- `Check transaction TXN001`
- `What is the refund status for TXN003?`

Type `quit` to exit.

### Demo Mode (8 preset queries)

```bash
python main.py --demo
```

### REST API Server

```bash
python main.py --api
```

Server starts at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/ask` | Main endpoint — natural language question |
| `GET` | `/transaction/{transaction_id}` | Direct transaction status lookup |
| `GET` | `/refund/{transaction_id}` | Direct refund status lookup |

### Example: POST `/ask`

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the refund status for TXN003?"}'
```

Response:
```json
{
  "question": "What is the refund status for TXN003?",
  "mode": "tool+rag",
  "tool_used": "check_refund_status",
  "answer": "Refund of ₹500 has been processed.\n\nPolicy context: ...",
  "sources": [...]
}
```

### Example: GET `/transaction/TXN001`

```bash
curl http://localhost:8000/transaction/TXN001
```

---

## Mock Transactions

The tools use a built-in mock dataset (no external API needed):

| TXN ID | Status | Method | Amount |
|--------|--------|--------|--------|
| TXN001 | failed | UPI | ₹1500 |
| TXN002 | success | Card | ₹2999 |
| TXN003 | refunded | Net Banking | ₹500 |
| TXN004 | pending | UPI | ₹750 |
| TXN005 | failed | Card | ₹3200 |
| TXN006 | success | Wallet | ₹199 |
| TXN007 | failed | Card | ₹4500 |
| TXN008 | refunded | UPI | ₹999 |

---

## Tech Stack

| Component | Library |
|-----------|---------|
| Embeddings | `sentence-transformers` |
| Vector search | `faiss-cpu` |
| RAG pipeline | `langchain`, `langchain-community` |
| API server | `fastapi`, `uvicorn` |
| Config | `python-dotenv` |
