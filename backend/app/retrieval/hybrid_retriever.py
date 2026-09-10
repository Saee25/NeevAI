from typing import Optional
from app.retrieval import vector_store
from app.retrieval.bm25_index import bm25_index
from app.models.retrieval import RetrievedChunk

COLLECTION_NAME = "corpus"

def retrieve(query: str, top_k: int = 5, category_filter: Optional[str] = None) -> list[RetrievedChunk]:
    """
    Combine dense (Qdrant) and sparse (BM25) results using Reciprocal Rank Fusion (RRF).
    """
    filter_dict = {"category": category_filter} if category_filter else None
    
    # Retrieve more documents initially to ensure a good intersection
    dense_results = vector_store.search(COLLECTION_NAME, query, top_k=top_k*2, filter_dict=filter_dict)
    sparse_results = bm25_index.search(query, top_k=top_k*2)
    
    # Filter sparse results by category if needed
    if category_filter:
        sparse_results = [res for res in sparse_results if res["payload"].get("category") == category_filter]
        
    # Apply RRF
    k = 60
    rrf_scores = {}
    
    # Process dense results
    for rank, res in enumerate(dense_results):
        text = res["payload"].get("text", "")
        if not text:
            continue
        if text not in rrf_scores:
            rrf_scores[text] = {"score": 0.0, "payload": res["payload"]}
        rrf_scores[text]["score"] += 1.0 / (k + rank + 1)
        
    # Process sparse results
    for rank, res in enumerate(sparse_results):
        text = res["payload"].get("text", "")
        if not text:
            continue
        if text not in rrf_scores:
            rrf_scores[text] = {"score": 0.0, "payload": res["payload"]}
        rrf_scores[text]["score"] += 1.0 / (k + rank + 1)
        
    # Sort by RRF score
    sorted_results = sorted(list(rrf_scores.values()), key=lambda x: x["score"], reverse=True)
    
    final_results = []
    for res in sorted_results[:top_k]:
        payload = res["payload"]
        final_results.append(RetrievedChunk(
            text=payload.get("text", ""),
            source=payload.get("source", "unknown"),
            url=payload.get("url", None),
            score=res["score"]
        ))
        
    return final_results
