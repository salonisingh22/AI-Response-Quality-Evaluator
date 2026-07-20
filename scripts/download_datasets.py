"""
Downloads TruthfulQA and SQuAD, and writes them into a single
normalized JSONL file that knowledge_base.py will consume.

Run from the project root:
    python scripts/download_datasets.py
"""

import os
import json
from datasets import load_dataset
import pandas as pd

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
OUTPUT_FILE = os.path.join(PROCESSED_DIR, "knowledge_base_source.jsonl")

# Cap SQuAD size so indexing later stays fast on a laptop.
# Increase this once the pipeline is working end-to-end.
SQUAD_SAMPLE_SIZE = 2000


def ensure_dirs():
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)


def load_truthfulqa():
    print("Downloading TruthfulQA...")

    url = "https://cdn.jsdelivr.net/gh/sylinrl/TruthfulQA@main/TruthfulQA.csv"
    df = pd.read_csv(url)

    docs = []
    for i, row in df.iterrows():
        docs.append({
            "doc_id": f"truthfulqa_{i}",
            "source": "truthfulqa",
            "question": row["Question"],
            "answer": row["Best Answer"],
            "context": row["Best Answer"],   # no passage, so answer IS the knowledge text
            "category": row.get("Category", "general"),
        })

    print(f"  -> {len(docs)} TruthfulQA docs")
    return docs


def load_squad():
    print("Downloading SQuAD...")
    ds = load_dataset("rajpurkar/squad")["train"]

    seen_contexts = set()
    docs = []
    for i, row in enumerate(ds):
        if len(docs) >= SQUAD_SAMPLE_SIZE:
            break
        # Skip duplicate contexts (SQuAD has many questions per passage)
        if row["context"] in seen_contexts:
            continue
        seen_contexts.add(row["context"])

        answer_text = row["answers"]["text"][0] if row["answers"]["text"] else ""
        docs.append({
            "doc_id": f"squad_{i}",
            "source": "squad",
            "question": row["question"],
            "answer": answer_text,
            "context": row["context"],       # the real passage
            "category": row.get("title", "general"),
        })

    print(f"  -> {len(docs)} SQuAD docs")
    return docs


def main():
    ensure_dirs()

    truthfulqa_docs = load_truthfulqa()
    squad_docs = load_squad()

    # Save raw copies too, for transparency / debugging
    with open(os.path.join(RAW_DIR, "truthfulqa_raw.json"), "w", encoding="utf-8") as f:
        json.dump(truthfulqa_docs, f, indent=2)
    with open(os.path.join(RAW_DIR, "squad_raw.json"), "w", encoding="utf-8") as f:
        json.dump(squad_docs, f, indent=2)

    all_docs = truthfulqa_docs + squad_docs

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for doc in all_docs:
            f.write(json.dumps(doc) + "\n")

    print(f"\nDone. {len(all_docs)} total documents written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
