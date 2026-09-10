import json
import os
import glob
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CORPUS_DIR = DATA_DIR / "corpus"
GLOSSARY_FILE = DATA_DIR / "glossary.json"

def build_chunking_pipeline():
    """
    Reads the corpus and glossary, chunks them appropriately, 
    and prepares data for embedding.
    """
    if not CORPUS_DIR.exists():
        print("Corpus directory not found. Please run fetch_corpus.py first.")
        return []

    documents_to_embed = []

    # Text splitter config: ~300-500 tokens with overlap
    # Assuming ~4 characters per token: 400 tokens = ~1600 characters
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1600,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    # 1. Process standard corpus files (JSONL)
    corpus_files = glob.glob(str(CORPUS_DIR / "*.jsonl"))
    for file_path in corpus_files:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    text = data.get("text", "")
                    if not text:
                        continue

                    # Chunk the text
                    chunks = text_splitter.split_text(text)
                    
                    for i, chunk in enumerate(chunks):
                        documents_to_embed.append({
                            "text": chunk,
                            "metadata": {
                                "source": data.get("source"),
                                "title": data.get("title"),
                                "category": data.get("category"),
                                "url": data.get("url"),
                                "chunk_index": i,
                                "type": "corpus"
                            }
                        })
                except json.JSONDecodeError:
                    print(f"Skipping malformed JSONL in {file_path}")

    # 2. Process Glossary
    if GLOSSARY_FILE.exists():
        with open(GLOSSARY_FILE, "r", encoding="utf-8") as f:
            try:
                glossary = json.load(f)
                for item in glossary:
                    term = item.get("term", "")
                    definition = item.get("short_definition", "")
                    if not term or not definition:
                        continue
                    
                    # Glossary items are usually short enough to not need chunking
                    text = f"{term}: {definition}"
                    documents_to_embed.append({
                        "text": text,
                        "metadata": {
                            "source": "glossary",
                            "title": term,
                            "category": "definition",
                            "type": "glossary"
                        }
                    })
            except json.JSONDecodeError:
                print(f"Error parsing {GLOSSARY_FILE}")

    print(f"Pipeline complete. Prepared {len(documents_to_embed)} chunks for embedding.")
    return documents_to_embed

import sys
from backend.app.retrieval import vector_store
from backend.app.retrieval.bm25_index import bm25_index

if __name__ == "__main__":
    chunks = build_chunking_pipeline()
    if not chunks:
        print("No chunks to process.")
        sys.exit(0)
        
    COLLECTION_NAME = "corpus"
    
    print("Initializing Qdrant collection...")
    # bge-small-en-v1.5 has vector size 384
    vector_store.init_collection(COLLECTION_NAME, vector_size=384)
    
    print("Upserting chunks to Qdrant (this may take a while)...")
    # Batch upsert to avoid huge requests
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        vector_store.upsert_chunks(COLLECTION_NAME, batch)
        print(f"Upserted {min(i+batch_size, len(chunks))}/{len(chunks)} chunks to Qdrant.")
        
    print("Building and saving BM25 index...")
    bm25_index.build_index(chunks)
    
    print(f"Successfully indexed {len(chunks)} chunks into both Qdrant and BM25.")
