"""
Embedding wrapper around a Hugging Face sentence-transformers model.

Keeps model loading in one place, and gives retriever.py a simple
text -> vector interface without needing to know model internals.
"""

from sentence_transformers import SentenceTransformer
from src.utils.config import EMBEDDING_MODEL_NAME as MODEL_NAME

_model = None  # loaded lazily, once, and reused (avoids reloading on every call)


def get_model():
    """
    Loads the embedding model once and caches it in memory.
    """
    global _model

    if _model is None:
        print(f"Loading embedding model: {MODEL_NAME} ...")
        _model = SentenceTransformer(MODEL_NAME)
        print("Embedding model loaded.")

    return _model


def embed_texts(texts):
    """
    Embeds a list of strings.

    Args:
        texts (list[str])

    Returns:
        list[list[float]]: one embedding vector per input text
    """
    model = get_model()
    embeddings = model.encode(
        texts,
        show_progress_bar=len(texts) > 50,
        convert_to_numpy=True,
    )
    return embeddings.tolist()


def embed_query(text):
    """
    Embeds a single query string (convenience wrapper for retriever.py).

    Returns:
        list[float]: embedding vector
    """
    return embed_texts([text])[0]


if __name__ == "__main__":
    sample_texts = [
        "Watermelon seeds pass through your digestive system.",
        "The Eiffel Tower is located in Paris, France.",
    ]

    vectors = embed_texts(sample_texts)

    print(f"Embedded {len(vectors)} texts.")
    print(f"Vector dimension: {len(vectors[0])}")
    print(f"First 5 values of vector 1: {vectors[0][:5]}")