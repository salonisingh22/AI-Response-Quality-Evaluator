"""
Knowledge Base loader.

Reads the normalized dataset (data/processed/knowledge_base_source.jsonl)
produced by scripts/download_datasets.py and exposes it as a list of
document dicts ready for chunking + embedding in retriever.py.
"""

import os
import json

from src.utils.config import KNOWLEDGE_BASE_SOURCE_PATH as KNOWLEDGE_BASE_PATH


def load_documents(path=KNOWLEDGE_BASE_PATH):
    """
    Loads the knowledge base JSONL file.

    Returns:
        list[dict]: each dict has:
            - id (str)
            - text (str)      -> the passage/context to embed & search over
            - question (str)
            - answer (str)
            - source (str)    -> 'truthfulqa' or 'squad'
            - category (str)
    """

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Knowledge base file not found at '{path}'. "
            "Run 'python scripts/download_datasets.py' first."
        )

    documents = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            row = json.loads(line)

            documents.append({
                "id": row["doc_id"],
                "text": row["context"],
                "question": row.get("question", ""),
                "answer": row.get("answer", ""),
                "source": row.get("source", "unknown"),
                "category": row.get("category", "general"),
            })

    return documents


def get_stats(documents):
    """
    Small helper for sanity-checking the loaded knowledge base.

    Returns:
        dict: counts per source, and total document count.
    """

    stats = {"total": len(documents)}

    for doc in documents:
        src = doc