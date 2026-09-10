import os
from typing import TypedDict, Optional, List
from pydantic import BaseModel, Field

class MarketFindings(BaseModel):
    tam_estimate: str = Field(description="Total Addressable Market estimate based on retrieved cases")
    sam_estimate: str = Field(description="Serviceable Addressable Market estimate based on retrieved cases")
    som_estimate: str = Field(description="Serviceable Obtainable Market estimate based on retrieved cases")
    reasoning: str = Field(description="Reasoning based on the retrieved cases. Note if retrieval is weak.")
    sources: List[str] = Field(description="List of source URLs or citations used")

class SimilarStartup(BaseModel):
    name: str
    outcome: str = Field(description="Success, failure, or current status")
    summary: str
    source_url: str

class CompetitorFindings(BaseModel):
    similar_startups: List[SimilarStartup]
    positioning_notes: str

class RiskFindings(BaseModel):
    market_risk: int = Field(ge=1, le=5, description="Market risk score 1-5")
    execution_risk: int = Field(ge=1, le=5, description="Execution risk score 1-5")
    funding_risk: int = Field(ge=1, le=5, description="Funding risk score 1-5")
    regulatory_risk: int = Field(ge=1, le=5, description="Regulatory risk score 1-5")
    notes: List[str] = Field(description="Reasoning notes citing specific chunks")

class FinalReport(BaseModel):
    readiness_score: int = Field(ge=0, le=100)
    summary: str
    market_findings: Optional[MarketFindings] = None
    competitor_findings: Optional[CompetitorFindings] = None
    risk_findings: Optional[RiskFindings] = None
    unverified_claims: List[str] = Field(default_factory=list)

class ValidationState(TypedDict):
    idea_text: str
    market_findings: Optional[MarketFindings]
    competitor_findings: Optional[CompetitorFindings]
    risk_findings: Optional[RiskFindings]
    final_report: Optional[FinalReport]

class PitchOutline(BaseModel):
    problem: str
    solution: str
    market_size: str
    competitive_edge: str
    ask: str

class InvestorMatch(BaseModel):
    name: str
    firm: str
    sector: str
    stage: str
    description: str
    match_reason: str
    disclaimer: str = "Sample match \u2014 verify current details before reaching out"

class OutreachDraft(BaseModel):
    subject: str
    body: str
