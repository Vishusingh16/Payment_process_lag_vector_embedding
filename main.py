"""
CLI entry point for the Payment Support RAG Agent.

Usage:
  python main.py                    # interactive mode
  python main.py --api              # start FastAPI server
  python main.py --demo             # run all 8 demo queries
"""

import sys
import argparse
import json
from src.agent import run_agent


def print_result(result: dict) -> None:
    print("\n" + "=" * 60)
    print(f"Q: {result['question']}")
    print(f"\nMode : {result['mode']}")
    if result.get("tool_used"):
        print(f"Tool : {result['tool_used']}")
    print(f"\nA: {result['answer']}")
    if result.get("sources"):
        print("\nSources retrieved:")
        for s in result["sources"]:
            print(f"  - [{s['category']}] {s['issue']}  (score: {s['score']:.4f})")
    print("=" * 60)


DEMO_QUERIES = [
    "My UPI payment failed but money was deducted. What should I do?",
    "How long does a refund take?",
    "What is the timeline for dispute resolution?",
    "Check transaction TXN001",
    "What is the refund status for TXN003?",
    "My card payment was declined. Why?",
    "I was charged twice for the same order. What happens now?",
    "What is a chargeback and how does it work?",
]


def run_demo() -> None:
    print("Running demo queries...\n")
    for q in DEMO_QUERIES:
        result = run_agent(q)
        print_result(result)


def run_interactive() -> None:
    print("Payment Support RAG Agent — type 'quit' to exit\n")
    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if not question:
            continue
        if question.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        result = run_agent(question)
        print_result(result)


def run_api() -> None:
    import uvicorn
    from src.api import app
    uvicorn.run(app, host="0.0.0.0", port=8000)


def main() -> None:
    parser = argparse.ArgumentParser(description="Payment Support RAG Agent")
    parser.add_argument("--api", action="store_true", help="Start FastAPI server on port 8000")
    parser.add_argument("--demo", action="store_true", help="Run demo queries")
    args = parser.parse_args()

    if args.api:
        run_api()
    elif args.demo:
        run_demo()
    else:
        run_interactive()


if __name__ == "__main__":
    main()
