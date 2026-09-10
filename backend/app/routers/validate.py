from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.app.agents.models import ScalingGuidance
from backend.app.agents.scaling_agent import ScalingAgent

router = APIRouter(prefix="/validate", tags=["validate"])

scaling_agent = ScalingAgent()

class ScalingAdviceRequest(BaseModel):
    idea_text: str
    revenue_context: Optional[str] = ""

@router.post("/scaling-advice", response_model=ScalingGuidance)
def get_scaling_advice(req: ScalingAdviceRequest):
    try:
        return scaling_agent.generate_advice(req.idea_text, req.revenue_context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
