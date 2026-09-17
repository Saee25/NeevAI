import os
import json
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# Load Kaggle Token from .env before importing kaggle
load_dotenv()
if "KAGGLE_API_TOKEN" not in os.environ and "KAGGLE_USERNAME" not in os.environ:
    print("WARNING: Kaggle credentials not found in environment.")

import kaggle

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CORPUS_DIR = DATA_DIR / "corpus"
OUTPUT_FILE = CORPUS_DIR / "structured_data.jsonl"

def main():
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    
    dataset = "manishkc06/startup-success-prediction"
    print(f"Downloading dataset {dataset}...")
    
    # Download the dataset
    kaggle.api.dataset_download_files(dataset, path=".", unzip=True)
    
    # Find the downloaded CSV
    csv_files = list(Path('.').glob('*.csv'))
    if not csv_files:
        print("No CSV file found after downloading.")
        return
        
    # We will prioritize 'startup_data.csv' if it exists, else use the first one
    csv_file = next((f for f in csv_files if 'startup_data.csv' in f.name), csv_files[0])
    print(f"Processing {csv_file}...")
    
    df = pd.read_csv(csv_file)
    
    records = []
    
    # Map each row to the natural language schema
    for idx, row in df.iterrows():
        # Fallbacks for missing columns
        name = str(row.get('name', 'A startup')).strip()
        if name.lower() == 'nan': name = 'A startup'
        
        sector = str(row.get('category_code', 'technology')).strip()
        if sector.lower() == 'nan': sector = 'technology'
            
        funding = str(row.get('funding_total_usd', 'undisclosed amount')).strip()
        if funding.lower() == 'nan' or funding == '-': funding = 'an undisclosed amount'
        else:
            try:
                # Basic formatting for large numbers if it's numeric
                funding = f"${float(funding):,.0f}"
            except ValueError:
                pass
                
        outcome = str(row.get('status', 'operating')).strip()
        if outcome.lower() == 'nan': outcome = 'operating'
        
        # Natural language text
        text = f"{name} was a {sector} startup that raised {funding} in funding before being {outcome}."
        
        record = {
            "source": "Kaggle Startup Success Dataset",
            "title": name,
            "category": "industry-data",
            "url": f"https://www.kaggle.com/datasets/{dataset}",
            "text": text
        }
        records.append(record)
        
    print(f"Mapped {len(records)} rows. Writing to {OUTPUT_FILE}...")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for r in records:
            f.write(json.dumps(r) + '\n')
            
    print("Done!")

if __name__ == "__main__":
    main()
