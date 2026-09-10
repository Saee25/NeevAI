from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agents.models import FinalReport, PitchOutline, InvestorMatch, OutreachDraft
from app.agents.generation_agents import PitchOutlineAgent, OutreachDraftAgent
from app.agents.investor_matcher import InvestorMatcher
from typing import List

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
def generate_pitch_outline(req: PitchRequest):
    try:
        return pitch_agent.generate(req.report)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/investor-matches", response_model=List[InvestorMatch])
def generate_investor_matches(req: MatchRequest):
    try:
        return investor_matcher.match(req.report)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/outreach-draft", response_model=OutreachDraft)
def generate_outreach_draft(req: OutreachRequest):
    try:
        return outreach_agent.generate(req.report, req.investor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
