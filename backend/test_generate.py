import asyncio
from app.agents.models import FinalReport, MarketFindings, CompetitorFindings, RiskFindings, SimilarStartup
from app.agents.generation_agents import PitchOutlineAgent, OutreachDraftAgent
from app.agents.investor_matcher import InvestorMatcher

async def test():
    print("Setting up test data...")
    report = FinalReport(
        readiness_score=75,
        summary="A B2B SaaS platform for automating compliance in the fintech sector using AI-driven document analysis.",
        market_findings=MarketFindings(
            tam_estimate="$10B globally by 2028",
            sam_estimate="$2B in US and Europe",
            som_estimate="$50M initial target",
            reasoning="Based on recent reports of regtech growth and compliance automation adoption.",
            sources=["https://example.com/report"]
        ),
        competitor_findings=CompetitorFindings(
            similar_startups=[
                SimilarStartup(name="ComplyAI", outcome="Series B", summary="Automated compliance for enterprise", source_url="https://complyai.example")
            ],
            positioning_notes="Focuses on mid-market fintechs, a relatively underserved segment compared to enterprise."
        ),
        risk_findings=RiskFindings(
            market_risk=2,
            execution_risk=4,
            funding_risk=3,
            regulatory_risk=5,
            notes=["High regulatory risk due to the nature of compliance."]
        ),
        unverified_claims=[]
    )

    print("\n--- Testing PitchOutlineAgent ---")
    pitch_agent = PitchOutlineAgent()
    pitch = pitch_agent.generate(report)
    print(pitch.model_dump_json(indent=2))

    print("\n--- Testing InvestorMatcher ---")
    matcher = InvestorMatcher()
    matches = matcher.match(report)
    for m in matches:
        print(m.model_dump_json(indent=2))

    if matches:
        print("\n--- Testing OutreachDraftAgent ---")
        outreach_agent = OutreachDraftAgent()
        draft = outreach_agent.generate(report, matches[0])
        print(draft.model_dump_json(indent=2))
    else:
        print("\nNo investor matches found to test outreach draft.")

if __name__ == "__main__":
    asyncio.run(test())
