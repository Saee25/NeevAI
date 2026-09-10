from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, Dict
from app.agents.models import ScalingGuidance, FinalReport
from app.agents.scaling_agent import ScalingAgent
from app.agents.graph import run_validation
from app.middleware.rate_limit import limiter
import re
from cachetools import LRUCache

router = APIRouter(prefix="/validate", tags=["validate"])

scaling_agent = ScalingAgent()

# Simple in-memory cache
# Key: normalized idea_text, Value: FinalReport
_validation_cache: LRUCache = LRUCache(maxsize=100)

class ValidateRequest(BaseModel):
    idea_text: str

class ScalingAdviceRequest(BaseModel):
    idea_text: str
    revenue_context: Optional[str] = ""

def _normalize_text(text: str) -> str:
    # Lowercase and remove extra whitespace
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

@router.post("/", response_model=FinalReport)
@limiter.limit("5/minute")
def validate_idea(request: Request, req: ValidateRequest):
    try:
        normalized_idea = _normalize_text(req.idea_text)
        
        # Check cache
        if normalized_idea in _validation_cache:
            return _validation_cache[normalized_idea]
            
        # Run validation
        report = run_validation(req.idea_text)
        
        # Save to cache
        _validation_cache[normalized_idea] = report
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to validate idea: {str(e)}")

@router.post("/scaling-advice", response_model=ScalingGuidance)
@limiter.limit("5/minute")
def get_scaling_advice(request: Request, req: ScalingAdviceRequest):
    try:
        return scaling_agent.generate_advice(req.idea_text, req.revenue_context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate scaling advice: {str(e)}")
