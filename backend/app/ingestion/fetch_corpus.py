import json
import os
import glob
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CORPUS_DIR = DATA_DIR / "corpus"
RAW_CASE_STUDIES_FILE = DATA_DIR / "corpus_case_studies.json"
RAW_ESSAYS_FILE = DATA_DIR / "corpus_essays.json"

def ensure_dirs():
    """Ensure that the data and corpus directories exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)

def assemble_corpus():
    """
    Reads manually created JSON files with case studies and essays,
    formats them consistently, and saves each entry as an individual JSONL 
    file in the corpus directory.
    """
    ensure_dirs()
    
    docs_processed = 0

    # 1. Process Case Studies
    if RAW_CASE_STUDIES_FILE.exists():
        with open(RAW_CASE_STUDIES_FILE, "r", encoding="utf-8") as f:
            try:
                case_studies = json.load(f)
                for i, doc in enumerate(case_studies):
                    # Enforce schema: {source, title, category, url, text}
                    formatted = {
                        "source": doc.get("source", "case_study"),
                        "title": doc.get("title", f"Case Study {i+1}"),
                        "category": doc.get("category", "startup_postmortem"),
                        "url": doc.get("url", ""),
                        "text": doc.get("text", "")
                    }
                    
                    if not formatted["text"]:
                        continue
                    
                    filename = CORPUS_DIR / f"case_study_{i}.jsonl"
                    with open(filename, "w", encoding="utf-8") as out_f:
                        out_f.write(json.dumps(formatted) + "\n")
                    docs_processed += 1
            except json.JSONDecodeError:
                print(f"Error parsing {RAW_CASE_STUDIES_FILE}")

    # 2. Process Essays
    if RAW_ESSAYS_FILE.exists():
        with open(RAW_ESSAYS_FILE, "r", encoding="utf-8") as f:
            try:
                essays = json.load(f)
                for i, doc in enumerate(essays):
                    formatted = {
                        "source": doc.get("source", "strategy_essay"),
                        "title": doc.get("title", f"Strategy Essay {i+1}"),
                        "category": doc.get("category", "strategy"),
                        "url": doc.get("url", ""),
                        "text": doc.get("text", "")
                    }
                    
                    if not formatted["text"]:
                        continue

                    filename = CORPUS_DIR / f"essay_{i}.jsonl"
                    with open(filename, "w", encoding="utf-8") as out_f:
                        out_f.write(json.dumps(formatted) + "\n")
                    docs_processed += 1
            except json.JSONDecodeError:
                print(f"Error parsing {RAW_ESSAYS_FILE}")

    print(f"Corpus assembly complete. Processed {docs_processed} documents.")

if __name__ == "__main__":
    assemble_corpus()
