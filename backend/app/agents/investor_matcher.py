import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List
from .models import FinalReport, InvestorMatch
from .llm import get_llm
from pydantic import BaseModel

class StartupProfile(BaseModel):
    inferred_stage: str
    inferred_sector: str

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

class InvestorMatcher:
    def __init__(self, data_dir="backend/app/data"):
        self.data_dir = data_dir
        self.model = SentenceTransformer('BAAI/bge-small-en-v1.5')
        self.investors = self._load_investors()
        
        self.investor_sector_embeddings = []
        for inv in self.investors:
            sector_text = " ".join(inv.get("sector_focus", []))
            self.investor_sector_embeddings.append(self.model.encode(sector_text))
            
    def _load_investors(self):
        # try multiple paths for test execution flexibility
        possible_paths = [
            os.path.join(self.data_dir, "investors.json"),
            "app/data/investors.json",
            "../data/investors.json",
            "backend/app/data/investors.json",
            "c:/Users/Saisha Productions M/Desktop/NeevAI/backend/app/data/investors.json"
        ]
        for p in possible_paths:
            if os.path.exists(p):
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
        raise FileNotFoundError("investors.json not found in expected locations.")

    def _infer_profile(self, report: FinalReport) -> StartupProfile:
        llm = get_llm().with_structured_output(StartupProfile)
        prompt = f"""
        Analyze this startup idea validation report and infer its current funding stage (e.g., pre-seed, seed, series a) 
        and its primary sector. If it's just an idea, it is 'pre-seed'.
        
        Summary: {report.summary}
        """
        return llm.invoke(prompt)

    def match(self, report: FinalReport) -> List[InvestorMatch]:
        profile = self._infer_profile(report)
        idea_text = f"{report.summary} {profile.inferred_sector}"
        idea_embedding = self.model.encode(idea_text)
        
        similarities = [cosine_similarity(idea_embedding, emb) for emb in self.investor_sector_embeddings]
        
        ranked_indices = np.argsort(similarities)[::-1]
        
        stages_order = ["pre-seed", "seed", "pre-series a", "series a", "series b", "series c"]
        target_stage = profile.inferred_stage.lower()
        target_idx = -1
        for i, s in enumerate(stages_order):
            if s in target_stage:
                target_idx = i
                break
                
        matches = []
        for idx in ranked_indices:
            inv = self.investors[idx]
            inv_stages = [s.lower() for s in inv.get("stage_focus", [])]
            
            stage_ok = False
            for s in inv_stages:
                if s in target_stage or target_stage in s:
                    stage_ok = True
                    break
            
            if not stage_ok and target_idx != -1:
                for s in inv_stages:
                    if s in stages_order:
                        s_idx = stages_order.index(s)
                        if abs(s_idx - target_idx) <= 1:
                            stage_ok = True
                            break
                            
            if not stage_ok and len(matches) > 0:
                continue
                
            sim_score = similarities[idx]
            reason = f"Matched: {profile.inferred_stage} stage, {profile.inferred_sector}"
            if sim_score > 0.5:
                 reason += f" (High sector overlap)"
                 
            matches.append(InvestorMatch(
                name=inv["name"],
                firm=inv["firm"],
                sector=", ".join(inv.get("sector_focus", [])),
                stage=", ".join(inv.get("stage_focus", [])),
                description=inv.get("bio_snippet", ""),
                match_reason=reason,
                disclaimer="Sample match \u2014 verify current details before reaching out"
            ))
            
            if len(matches) >= 3:
                break
                
        # Fallback if strict filtering eliminated everything
        if not matches:
            for idx in ranked_indices[:3]:
                inv = self.investors[idx]
                matches.append(InvestorMatch(
                    name=inv["name"],
                    firm=inv["firm"],
                    sector=", ".join(inv.get("sector_focus", [])),
                    stage=", ".join(inv.get("stage_focus", [])),
                    description=inv.get("bio_snippet", ""),
                    match_reason=f"Matched primarily on sector similarity to {profile.inferred_sector}",
                    disclaimer="Sample match \u2014 verify current details before reaching out"
                ))
                
        return matches
