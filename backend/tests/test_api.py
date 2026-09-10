import os
os.environ["GROQ_API_KEY"] = "mock_key"
os.environ["GOOGLE_API_KEY"] = "mock_key"

from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.agents.models import FinalReport, PitchOutline, InvestorMatch, OutreachDraft, MarketFindings, CompetitorFindings, RiskFindings, SimilarStartup, ScalingGuidance, ScalingDirection, NotRecommended

client = TestClient(app)

# Helper mock data
mock_report = FinalReport(
    readiness_score=80,
    summary="A mock idea.",
    market_findings=MarketFindings(
        tam_estimate="$1B",
        sam_estimate="$500M",
        som_estimate="$10M",
        reasoning="Mock reasoning",
        sources=[]
    ),
    competitor_findings=CompetitorFindings(
        similar_startups=[],
        positioning_notes="Mock notes"
    ),
    risk_findings=RiskFindings(
        market_risk=2,
        execution_risk=2,
        funding_risk=2,
        regulatory_risk=2,
        notes=[]
    ),
    unverified_claims=[]
)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "AI Co-Founder API is running"}

@patch("app.routers.validate.run_validation")
def test_validate_idea(mock_run_validation):
    mock_run_validation.return_value = mock_report
    response = client.post("/validate/", json={"idea_text": "A test idea"})
    assert response.status_code == 200
    data = response.json()
    assert data["readiness_score"] == 80
    assert data["summary"] == "A mock idea."

@patch("app.routers.validate.scaling_agent.generate_advice")
def test_scaling_advice(mock_generate_advice):
    mock_generate_advice.return_value = ScalingGuidance(
        feasible_directions=[ScalingDirection(direction="Up", reasoning="Because", sources=[])],
        not_recommended=[NotRecommended(direction="Down", reasoning="Bad idea")],
        disclaimer="Disclaimer"
    )
    response = client.post("/validate/scaling-advice", json={"idea_text": "A test idea", "revenue_context": "We make $1M"})
    assert response.status_code == 200
    data = response.json()
    assert "feasible_directions" in data

@patch("app.routers.generate.pitch_agent.generate")
def test_pitch_outline(mock_pitch_generate):
    mock_pitch_generate.return_value = PitchOutline(
        problem="Problem",
        solution="Solution",
        market_size="Market",
        competitive_edge="Edge",
        ask="Ask"
    )
    response = client.post("/generate/pitch-outline", json={"report": mock_report.model_dump()})
    assert response.status_code == 200
    data = response.json()
    assert data["problem"] == "Problem"

@patch("app.routers.generate.investor_matcher.match")
def test_investor_matches(mock_matcher):
    mock_matcher.return_value = [
        InvestorMatch(
            name="Mock Capital",
            firm="Mock VC",
            sector="SaaS",
            stage="Seed",
            description="A VC firm",
            match_reason="Good match"
        )
    ]
    response = client.post("/generate/investor-matches", json={"report": mock_report.model_dump()})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Mock Capital"

@patch("app.routers.generate.outreach_agent.generate")
def test_outreach_draft(mock_outreach_generate):
    mock_outreach_generate.return_value = OutreachDraft(
        subject="Mock Subject",
        body="Mock Body"
    )
    investor = InvestorMatch(
        name="Mock Capital",
        firm="Mock VC",
        sector="SaaS",
        stage="Seed",
        description="A VC firm",
        match_reason="Good match"
    )
    response = client.post("/generate/outreach-draft", json={"report": mock_report.model_dump(), "investor": investor.model_dump()})
    assert response.status_code == 200
    data = response.json()
    assert data["subject"] == "Mock Subject"
    assert data["body"] == "Mock Body"
