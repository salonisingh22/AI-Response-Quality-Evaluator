"""
Central configuration for the RAG pipeline.
Adjust values here rather than hardcoding them across files.
"""

# Embedding model
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Chunking
CHUNK_SIZE = 300      # max words per chunk
CHUNK_OVERLAP = 50    # overlapping words between consecutive chunks

# Retrieval
DEFAULT_TOP_K = 1     # how many chunks app.py retrieves for the Reference Answer box

# Storage paths
KNOWLEDGE_BASE_SOURCE_PATH = "data/processed/knowledge_base_source.jsonl"
CHROMA_DIR = "knowledge_base/chroma_store"
CHROMA_COLLECTION_NAME = "ai_evaluator_kb"