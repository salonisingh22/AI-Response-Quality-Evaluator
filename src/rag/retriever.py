"""
Retriever: chunking + ChromaDB indexing + semantic search.

Builds a persistent vector index from the knowledge base (once), then
lets the rest of the app retrieve the most relevant chunk(s) for a
given question.
"""

import chromadb

from src.rag.knowledge_base import load_documents
from src.rag.embedding import embed_texts, embed_query
from src.utils.config import (
    CHROMA_DIR,
    CHROMA_COLLECTION_NAME as COLLECTION_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """
    Splits text into overlapping word-based chunks.

    Short texts (most TruthfulQA answers) return as a single chunk.
    Longer texts (SQuAD passages) get split so no single chunk is too
    large to embed meaningfully.
    """
    words = text.split()

    if len(words) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def get_client():
    return chromadb.PersistentClient(path=CHROMA_DIR)


def get_collection():
    client = get_client()
    return client.get_or_create_collection(name=COLLECTION_NAME)


def build_index(force_rebuild=False):
    """
    Builds (or rebuilds) the ChromaDB index from the knowledge base.

    Safe to call multiple times: if the collection already has data
    and force_rebuild=False, it skips re-indexing.
    """
    collection = get_collection()

    if collection.count() > 0 and not force_rebuild:
        print(f"Index already exists with {collection.count()} chunks. Skipping build.")
        return collection

    if force_rebuild and collection.count() > 0:
        client = get_client()
        client.delete_collection(COLLECTION_NAME)
        collection = get_client().get_or_create_collection(name=COLLECTION_NAME)

    print("Building index from knowledge base...")
    documents = load_documents()

    all_chunk_texts = []
    all_chunk_ids = []
    all_chunk_metadata = []

    for doc in documents:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            all_chunk_texts.append(chunk)
            all_chunk_ids.append(f"{doc['id']}_chunk{i}")
            all_chunk_metadata.append({
                "source": doc["source"],
                "category": doc["category"],
                "question": doc["question"],
                "answer": doc["answer"],
            })

    print(f"Embedding {len(all_chunk_texts)} chunks (this may take a minute)...")

    batch_size = 256
    for start in range(0, len(all_chunk_texts), batch_size):
        end = start + batch_size
        batch_texts = all_chunk_texts[start:end]
        batch_ids = all_chunk_ids[start:end]
        batch_meta = all_chunk_metadata[start:end]

        batch_embeddings = embed_texts(batch_texts)

        collection.add(
            ids=batch_ids,
            embeddings=batch_embeddings,
            documents=batch_texts,
            metadatas=batch_meta,
        )
        print(f"  Indexed {min(end, len(all_chunk_texts))}/{len(all_chunk_texts)}")

    print(f"Index built. Total chunks: {collection.count()}")
    return collection


def retrieve(question, top_k=3):
    """
    Retrieves the top_k most semantically relevant chunks for a question.

    Returns:
        list[dict]: each with 'text', 'score' (similarity, higher=better),
                    and 'metadata' (source/category/question/answer)
    """
    collection = get_collection()

    if collection.count() == 0:
        raise RuntimeError(
            "Knowledge base index is empty. Run build_index() first "
            "(e.g. `python -m src.rag.retriever`)."
        )

    query_embedding = embed_query(question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    retrieved = []
    for i in range(len(results["ids"][0])):
        distance = results["distances"][0][i]
        similarity = 1 - distance  # Chroma returns cosine distance by default
        retrieved.append({
            "text": results["documents"][0][i],
            "score": round(similarity, 4),
            "metadata": results["metadatas"][0][i],
        })

    return retrieved


if __name__ == "__main__":
    build_index()

    test_question = "What happens if you eat watermelon seeds?"
    print(f"\nTest query: {test_question}\n")

    results = retrieve(test_question, top_k=3)
    for i, r in enumerate(results, 1):
        print(f"{i}. [score={r['score']}] ({r['metadata']['source']})")
        print(f"   {r['text'][:150]}")
        print()