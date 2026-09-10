import os
import pickle
import re
from rank_bm25 import BM25Okapi

BM25_INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "bm25_index.pkl")

class BM25Retriever:
    def __init__(self):
        self.bm25 = None
        self.corpus = []
        self._load_index()
        
    def _load_index(self):
        if os.path.exists(BM25_INDEX_PATH):
            with open(BM25_INDEX_PATH, "rb") as f:
                data = pickle.load(f)
                self.bm25 = data["bm25"]
                self.corpus = data["corpus"]

    def build_index(self, chunks: list[dict]):
        """
        Builds the BM25 index from a list of chunks and persists it.
        Each chunk is a dict with 'text' and 'metadata'.
        """
        self.corpus = chunks
        tokenized_corpus = [re.findall(r'\w+', chunk["text"].lower()) for chunk in chunks]
        self.bm25 = BM25Okapi(tokenized_corpus)
        
        # Save to disk
        os.makedirs(os.path.dirname(BM25_INDEX_PATH), exist_ok=True)
        with open(BM25_INDEX_PATH, "wb") as f:
            pickle.dump({"bm25": self.bm25, "corpus": self.corpus}, f)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """
        Searches the BM25 index for the top_k matching chunks.
        """
        if not self.bm25:
            return []
            
        tokenized_query = re.findall(r'\w+', query.lower())
        scores = self.bm25.get_scores(tokenized_query)
        
        # Get top k indices
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        
        results = []
        for i in top_indices:
            if scores[i] > 0:
                results.append({
                    "payload": {
                        "text": self.corpus[i]["text"],
                        **self.corpus[i].get("metadata", {})
                    },
                    "score": scores[i]
                })
        return results

# Singleton instance
bm25_index = BM25Retriever()
