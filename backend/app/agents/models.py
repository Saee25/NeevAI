import os
import re
from typing import TypedDict, Optional, List, Any
from pydantic import BaseModel, Field, ConfigDict, model_validator

class MarketFindings(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    tam_estimate: str = Field(default="", description="Total Addressable Market estimate based on retrieved cases")
    sam_estimate: str = Field(default="", description="Serviceable Addressable Market estimate based on retrieved cases")
    som_estimate: str = Field(default="", description="Serviceable Obtainable Market estimate based on retrieved cases")
    reasoning: str = Field(default="", description="Reasoning based on the retrieved cases. Note if retrieval is weak.")
    sources: List[str] = Field(default_factory=list, description="List of source URLs or citations used")

    @model_validator(mode="before")
    @classmethod
    def normalize_fields(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        res = dict(data)
        mapping = {
            "tam_estimate": ["TAM", "tam", "tamEstimate", "marketSizeEstimate", "market_size_estimate", "market_size", "marketSize"],
            "sam_estimate": ["SAM", "sam", "samEstimate", "sam_estimate"],
            "som_estimate": ["SOM", "som", "somEstimate", "som_estimate"],
            "reasoning": ["notes", "assessment", "qualitative_estimation", "confidence", "explanation", "analysis"],
            "sources": ["source", "citations", "references"]
        }
        for target, aliases in mapping.items():
            if not res.get(target):
                for alias in aliases:
                    if alias in res and res[alias]:
                        res[target] = str(res[alias]) if target != "sources" else res[alias]
                        break
        if isinstance(res.get("sources"), str):
            res["sources"] = [res["sources"]]
        elif not isinstance(res.get("sources"), list):
            res["sources"] = []
        return res

class SimilarStartup(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    name: str = Field(default="Unknown")
    outcome: str = Field(default="Unknown", description="Success, failure, or current status")
    summary: str = Field(default="")
    source_url: str = Field(default="")

    @model_validator(mode="before")
    @classmethod
    def normalize_fields(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        res = dict(data)
        if not res.get("source_url"):
            for a in ["url", "source", "link", "sourceUrl"]:
                if a in res and res[a]:
                    res["source_url"] = str(res[a])
                    break
        if not res.get("outcome"):
            for a in ["status", "result"]:
                if a in res and res[a]:
                    res["outcome"] = str(res[a])
                    break
        if not res.get("summary"):
            for a in ["description", "notes", "details"]:
                if a in res and res[a]:
                    res["summary"] = str(res[a])
                    break
        return res

class CompetitorFindings(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    similar_startups: List[SimilarStartup] = Field(default_factory=list)
    positioning_notes: str = Field(default="")

    @model_validator(mode="before")
    @classmethod
    def normalize_fields(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        res = dict(data)
        if not res.get("similar_startups"):
            for a in ["similarStartups", "competitors", "startups", "similar_companies"]:
                if a in res and isinstance(res[a], list):
                    res["similar_startups"] = res[a]
                    break
        if not res.get("positioning_notes"):
            for a in ["positioningNotes", "positioning", "notes", "summary"]:
                if a in res and res[a]:
                    res["positioning_notes"] = str(res[a])
                    break
        return res

class RiskFindings(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    market_risk: int = Field(default=3, ge=1, le=5, description="Market risk score 1-5")
    execution_risk: int = Field(default=3, ge=1, le=5, description="Execution risk score 1-5")
    funding_risk: int = Field(default=3, ge=1, le=5, description="Funding risk score 1-5")
    regulatory_risk: int = Field(default=3, ge=1, le=5, description="Regulatory risk score 1-5")
    notes: List[str] = Field(default_factory=list, description="Reasoning notes citing specific chunks")

    @model_validator(mode="before")
    @classmethod
    def normalize_fields(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        res = dict(data)
        for field in ["market_risk", "execution_risk", "funding_risk", "regulatory_risk"]:
            camel = "".join(word.capitalize() if i > 0 else word for i, word in enumerate(field.split("_")))
            if field not in res and camel in res:
                res[field] = res[camel]
            val = res.get(field)
            if isinstance(val, str):
                match = re.search(r'\d+', val)
                if match:
                    val = int(match.group())
                elif "high" in val.lower():
                    val = 4
                elif "low" in val.lower():
                    val = 2
                else:
                    val = 3
            if isinstance(val, (int, float)):
                res[field] = max(1, min(5, int(val)))
            elif val is None:
                res[field] = 3
        if isinstance(res.get("notes"), str):
            res["notes"] = [res["notes"]]
        elif not isinstance(res.get("notes"), list):
            res["notes"] = []
        return res

class FinalReport(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    readiness_score: int = Field(default=50, ge=0, le=100)
    summary: str = Field(default="")
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
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    problem: str = Field(default="")
    solution: str = Field(default="")
    market_size: str = Field(default="")
    competitive_edge: str = Field(default="")
    ask: str = Field(default="")

    @model_validator(mode="before")
    @classmethod
    def normalize_fields(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        res = dict(data)
        if not res.get("market_size") and "marketSize" in res:
            res["market_size"] = str(res["marketSize"])
        if not res.get("competitive_edge") and "competitiveEdge" in res:
            res["competitive_edge"] = str(res["competitiveEdge"])
        return res

class InvestorMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    name: str = Field(default="")
    firm: str = Field(default="")
    sector: str = Field(default="")
    stage: str = Field(default="")
    description: str = Field(default="")
    match_reason: str = Field(default="")
    disclaimer: str = "Sample match — verify current details before reaching out"

class OutreachDraft(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    subject: str = Field(default="")
    body: str = Field(default="")

class ScalingDirection(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    direction: str = Field(default="", description="The scaling direction or strategy.")
    reasoning: str = Field(default="", description="Qualitative reasoning for this direction.")
    sources: List[str] = Field(default_factory=list, description="List of source URLs or citations.")

    @model_validator(mode="before")
    @classmethod
    def normalize_fields(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        res = dict(data)
        if isinstance(res.get("sources"), str):
            res["sources"] = [res["sources"]]
        elif not isinstance(res.get("sources"), list):
            res["sources"] = []
        return res

class NotRecommended(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    direction: str = Field(default="", description="The scaling direction that is not recommended.")
    reasoning: str = Field(default="", description="Reasoning for why it is not recommended.")

class ScalingGuidance(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    feasible_directions: List[ScalingDirection] = Field(default_factory=list, description="List of feasible scaling directions.")
    not_recommended: List[NotRecommended] = Field(default_factory=list, description="List of not recommended scaling directions.")
    disclaimer: str = Field(default="Informational analysis based on comparable cases, not financial or investment advice.")

    @model_validator(mode="before")
    @classmethod
    def normalize_fields(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        res = dict(data)
        if not res.get("feasible_directions") and "feasibleDirections" in res:
            res["feasible_directions"] = res["feasibleDirections"]
        if not res.get("not_recommended") and "notRecommended" in res:
            res["not_recommended"] = res["notRecommended"]
        return res
