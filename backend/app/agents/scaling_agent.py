from backend.app.agents.models import ScalingGuidance
from backend.app.retrieval.hybrid_retriever import retrieve
from backend.app.agents.llm import get_llm
from langchain_core.prompts import PromptTemplate

class ScalingAgent:
    def __init__(self):
        self.llm = get_llm()
        self.structured_llm = self.llm.with_structured_output(ScalingGuidance)

    def generate_advice(self, idea_text: str, revenue_context: str = "") -> ScalingGuidance:
        # Retrieve chunks filtered to category "scaling"
        query = f"scaling for {idea_text} {revenue_context}"
        chunks = retrieve(query=query, top_k=5, category_filter="scaling")
        
        # Fallback to general corpus if nothing found
        if not chunks:
            chunks = retrieve(query=query, top_k=5)
            
        context_text = "\n\n".join([f"Source: {c.source}\nContent: {c.text}" for c in chunks])
        
        prompt = PromptTemplate.from_template(
            """You are an expert startup scaling advisor. Analyze the business description and revenue context to provide scaling guidance based ONLY on the provided retrieved case studies.

STRICT INSTRUCTIONS:
You must never output a specific numeric recommendation (funding amount, price point, valuation, headcount number) as advice. You may cite numeric figures FROM RETRIEVED SOURCES as historical pattern evidence (e.g., 'similar-stage companies in retrieved cases raised in the ₹20L-1Cr range'), but never tell the user what number to target for their own decision. Frame all guidance as reasoning about what approaches are more or less common/feasible given retrieved evidence, and explicitly say when something appears impractical, with reasons.

Business Idea: {idea_text}
Revenue Context: {revenue_context}

Context from retrieved case studies:
{context}
"""
        )
        
        chain = prompt | self.structured_llm
        
        result = chain.invoke({
            "idea_text": idea_text,
            "revenue_context": revenue_context,
            "context": context_text
        })
        
        # Add actual sources if the LLM forgot to add them based on the context
        actual_sources = list(set([c.source for c in chunks if c.source]))
        for direction in result.feasible_directions:
            if not direction.sources:
                direction.sources = actual_sources
                
        return result
