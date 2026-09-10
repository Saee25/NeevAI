from sentence_transformers import SentenceTransformer

# Load model once at module level to avoid reload cost
MODEL_NAME = "BAAI/bge-small-en-v1.5"
_model = SentenceTransformer(MODEL_NAME)

def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Embed a list of texts using sentence-transformers.
    Returns a list of dense vectors.
    """
    if not texts:
        return []
    # sentence-transformers outputs numpy arrays, convert to list of lists for Qdrant
    embeddings = _model.encode(texts, normalize_embeddings=True)
    return embeddings.tolist()
