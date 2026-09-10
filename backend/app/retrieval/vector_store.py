import os
import uuid
from typing import Optional
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct, Filter
from backend.app.retrieval.embeddings import embed_texts

QDRANT_URL = os.environ.get("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY", None)

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

def init_collection(name: str, vector_size: int = 384):
    """
    Creates a collection if it does not exist.
    """
    if not client.collection_exists(collection_name=name):
        client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

def upsert_chunks(name: str, chunks: list[dict]):
    """
    Embeds and stores chunks with metadata in Qdrant.
    chunks is expected to be a list of dictionaries with 'text' and 'metadata'.
    """
    texts = [chunk["text"] for chunk in chunks]
    if not texts:
        return
    
    embeddings = embed_texts(texts)
    
    points = []
    for chunk, vector in zip(chunks, embeddings):
        payload = {"text": chunk["text"], **chunk.get("metadata", {})}
        point_id = str(uuid.uuid4())
        points.append(
            PointStruct(id=point_id, vector=vector, payload=payload)
        )
    
    if points:
        client.upsert(
            collection_name=name,
            points=points
        )

def search(name: str, query: str, top_k: int = 5, filter_dict: Optional[dict] = None) -> list[dict]:
    """
    Searches Qdrant for similar chunks.
    """
    query_vector = embed_texts([query])[0]
    
    qdrant_filter = None
    if filter_dict:
        from qdrant_client.http.models import FieldCondition, MatchValue
        conditions = [
            FieldCondition(key=k, match=MatchValue(value=v))
            for k, v in filter_dict.items()
        ]
        qdrant_filter = Filter(must=conditions)
        
    results = client.search(
        collection_name=name,
        query_vector=query_vector,
        limit=top_k,
        query_filter=qdrant_filter
    )
    
    return [{"payload": res.payload, "score": res.score} for res in results]
