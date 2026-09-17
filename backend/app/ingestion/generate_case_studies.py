import json
import wikipedia
import time
from pathlib import Path

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
CORPUS_DIR = DATA_DIR / "corpus"
OUTPUT_FILE = CORPUS_DIR / "corpus_case_studies.json"

startups = [
    ("Housing.com", "India", "proptech", "failed"),
    ("WeWork", "Global", "real estate", "failed"),
    ("Dukaan", "India", "ecommerce", "success"),
    ("Juicero", "Global", "hardware", "failed"),
    ("Freshworks", "India", "B2B SaaS", "success"),
    ("Theranos", "Global", "healthtech", "failed"),
    ("Zerodha", "India", "fintech", "success"),
    ("Quibi", "Global", "consumer social", "failed"),
    ("Zomato", "India", "marketplace", "success"),
    ("Pebble", "Global", "hardware", "failed"),
    ("Khatabook", "India", "B2B SaaS", "success"),
    ("Scale API", "Global", "B2B SaaS", "success"),
    ("DeHaat", "India", "agritech", "success"),
    ("AgroStar", "India", "agritech", "success"),
    ("Farmers Business Network", "Global", "agritech", "success"),
    ("Yik Yak", "Global", "consumer social", "failed"),
    ("ShareChat", "India", "consumer social", "success"),
    ("Meesho", "India", "marketplace", "success"),
    ("Jawbone", "Global", "hardware", "failed"),
    ("Ather Energy", "India", "hardware", "success"),
    ("Cure.fit", "India", "healthtech", "success"),
    ("Practo", "India", "healthtech", "success"),
    ("PharmEasy", "India", "healthtech", "success"),
    ("Color Genomics", "Global", "healthtech", "success"),
    ("Paytm", "India", "fintech", "success"),
    ("Stripe", "Global", "fintech", "success"),
    ("Razorpay", "India", "fintech", "success"),
    ("Robinhood", "Global", "fintech", "success"),
    ("Lenskart", "India", "D2C", "success"),
    ("Warby Parker", "Global", "D2C", "success"),
    ("Nykaa", "India", "D2C", "success"),
    ("Casper", "Global", "D2C", "success"),
    ("Swiggy", "India", "marketplace", "success"),
    ("Airbnb", "Global", "marketplace", "success"),
    ("Uber", "Global", "marketplace", "success"),
    ("Ola", "India", "marketplace", "success"),
    ("Pepperfry", "India", "marketplace", "success"),
    ("Stayzilla", "India", "marketplace", "failed"),
    ("Voonik", "India", "marketplace", "failed"),
    ("ShopClues", "India", "marketplace", "failed"),
    ("LocalBanya", "India", "ecommerce", "failed"),
    ("TinyOwl", "India", "foodtech", "failed"),
    ("Roadrunnr", "India", "logistics", "failed"),
    ("Grofers", "India", "marketplace", "success"), 
    ("Delhivery", "India", "logistics", "success"),
    ("Rivigo", "India", "logistics", "success"),
    ("Udaan", "India", "B2B marketplace", "success"),
    ("Postman", "India", "B2B SaaS", "success"),
    ("Notion", "Global", "B2B SaaS", "success"),
    ("Figma", "Global", "B2B SaaS", "success"),
]

def generate():
    case_studies = []
    
    print(f"Generating case studies...")
    
    for startup, region, sector, outcome in startups:
        print(f"\nProcessing: {startup} ({sector}) - Fetching Wikipedia...")
        
        try:
            # First search to get exact title
            search_query = f"{startup} company" if "startup" not in startup.lower() else startup
            search_results = wikipedia.search(search_query, results=1)
            
            if not search_results:
                print(f"  ! No Wikipedia page found for {startup}. Skipping.")
                continue
                
            page_title = search_results[0]
            
            # Fetch summary directly from wikipedia
            # The lead paragraph acts as a perfect 3-5 sentence factual analytical summary of the company
            summary = wikipedia.summary(page_title, sentences=4, auto_suggest=False)
            
            # Get the page to get the exact URL
            page = wikipedia.page(page_title, auto_suggest=False)
            
            if len(summary) < 50:
                print(f"  ! Summary too short for {startup}. Skipping.")
                continue
                
            print(f"  Fetched URL: {page.url}")
            
            # Derive category using simple keywords since LLM is too flaky
            cat = "scaling"
            if "fail" in summary.lower() or outcome == "failed":
                cat = "risk"
            elif "compet" in summary.lower():
                cat = "competition"
                
            case_studies.append({
                "startup": startup,
                "region": region,
                "sector": sector,
                "outcome": outcome,
                "summary": summary,
                "category": cat,
                "source_url": page.url
            })
            
            print(f"  Summary generated and categorized as '{cat}'")
            
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"  ! Disambiguation Error for {startup}. Options: {e.options[:3]}")
        except wikipedia.exceptions.PageError:
            print(f"  ! Wikipedia Page not found for {startup}.")
        except Exception as e:
            print(f"  ! Error processing {startup}: {e}")
            
        time.sleep(1) # Be polite to Wikipedia
        
    print(f"\nWriting {len(case_studies)} case studies to {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(case_studies, f, indent=2)
        
    print("\n========================================")
    print("VERIFICATION - URLs USED:")
    print("========================================")
    for c in case_studies:
        print(f"- {c['startup']}: {c['source_url']}")

if __name__ == "__main__":
    generate()
