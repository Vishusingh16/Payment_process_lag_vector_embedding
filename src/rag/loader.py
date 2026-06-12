import re


def load_and_chunk(filepath: str) -> list[dict]:
    """
    Reads the support_policies.txt file.
    Each block starts with a [CATEGORY] tag followed by Issue/Description/Resolution.
    Returns a list of chunk dicts with id, category, issue, and full text.
    """
    with open(filepath, "r") as f:
        raw = f.read()

    # Split on [CATEGORY] markers
    blocks = re.split(r"\n(?=\[)", raw.strip())

    chunks = []
    for i, block in enumerate(blocks):
        if not block.strip():
            continue

        category_match = re.match(r"\[(\w+)\]", block.strip())
        category = category_match.group(1) if category_match else "UNKNOWN"

        issue_match = re.search(r"Issue:\s*(.+)", block)
        issue = issue_match.group(1).strip() if issue_match else ""

        # Collapse multiple newlines for clean embedding text
        clean_text = " ".join(block.split())

        chunks.append({
            "id": i,
            "category": category,
            "issue": issue,
            "text": clean_text,
        })

    return chunks




  #{
 #"id":1,
  #"category":"PAYMENT_FAILURE",
 # "issue":"Insufficient Balance",
 #  "text":"..."
  #},

 # ...
#]