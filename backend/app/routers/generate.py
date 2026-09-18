from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.agents.models import FinalReport, PitchOutline, InvestorMatch, OutreachDraft
from app.agents.generation_agents import PitchOutlineAgent, OutreachDraftAgent
from app.agents.investor_matcher import InvestorMatcher
from app.middleware.rate_limit import limiter
from typing import List
import traceback

router = APIRouter(prefix="/generate", tags=["generation"])

pitch_agent = PitchOutlineAgent()
investor_matcher = InvestorMatcher()
outreach_agent = OutreachDraftAgent()

class PitchRequest(BaseModel):
    report: FinalReport

class MatchRequest(BaseModel):
    report: FinalReport

class OutreachRequest(BaseModel):
    report: FinalReport
    investor: InvestorMatch

@router.post("/pitch-outline", response_model=PitchOutline)
@limiter.limit("10/minute")
def generate_pitch_outline(request: Request, req: PitchRequest):
    try:
        print("\n📄 [Pitch Outline] Generating 1-page structured pitch outline from validation report...")
        outline = pitch_agent.generate(req.report)
        print("   ✓ Pitch outline generated successfully.")
        return outline
    except Exception as e:
        print(f"\n❌ [Error] Failed to generate pitch outline: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to generate pitch outline: {str(e)}")

@router.post("/investor-matches", response_model=List[InvestorMatch])
@limiter.limit("10/minute")
def generate_investor_matches(request: Request, req: MatchRequest):
    try:
        print("\n🤝 [Investor Matcher] Finding top matching investors by stage and sector...")
        matches = investor_matcher.match(req.report)
        print(f"   ✓ Matched {len(matches)} investor(s).")
        return matches
    except Exception as e:
        print(f"\n❌ [Error] Failed to find investor matches: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to find investor matches: {str(e)}")

@router.post("/outreach-draft", response_model=OutreachDraft)
@limiter.limit("10/minute")
def generate_outreach_draft(request: Request, req: OutreachRequest):
    try:
        print(f"\n✉️ [Outreach Draft] Drafting personalized cold email for {req.investor.name} ({req.investor.firm})...")
        draft = outreach_agent.generate(req.report, req.investor)
        print(f"   ✓ Cold email draft generated: \"{draft.subject}\"")
        return draft
    except Exception as e:
        print(f"\n❌ [Error] Failed to generate outreach draft: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to generate outreach draft: {str(e)}")
