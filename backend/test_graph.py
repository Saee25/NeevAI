import os
import sys

# Add backend to path so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.agents.graph import run_validation

def test():
    ideas = [
        "A platform that uses AI to generate personalized workout plans based on a user's DNA profile.",
        "A marketplace for buying and selling fractional shares of commercial real estate.",
    ]
    
    for idea in ideas:
        print("=========================================")
        print(f"Testing Idea: {idea}")
        print("=========================================")
        try:
            report = run_validation(idea)
            print("Readiness Score:", report.readiness_score)
            print("Summary:\n", report.summary)
            print("Unverified Claims:\n", report.unverified_claims)
            if report.market_findings:
                print("TAM Estimate:", report.market_findings.tam_estimate)
            if report.competitor_findings:
                print("Competitors Found:", len(report.competitor_findings.similar_startups))
        except Exception as e:
            print(f"Error testing idea: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test()
