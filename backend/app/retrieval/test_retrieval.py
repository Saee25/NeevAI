from backend.app.retrieval.hybrid_retriever import retrieve

def test():
    queries = [
        "fintech startup that failed due to regulatory issues",
        "how to scale an enterprise SaaS business",
        "market size of the creator economy"
    ]
    
    for query in queries:
        print(f"\n{'='*50}\nQuery: {query}\n{'='*50}")
        results = retrieve(query, top_k=5)
        
        if not results:
            print("No results found.")
            continue
            
        for i, res in enumerate(results):
            print(f"\n--- Result {i+1} (Score: {res.score:.4f}) ---")
            print(f"Source: {res.source}")
            if res.url:
                print(f"URL: {res.url}")
            print(f"Text snippet: {res.text[:200]}...")

if __name__ == "__main__":
    test()
