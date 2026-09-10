from app.agents.models import ValidationState, MarketFindings
from app.retrieval.hybrid_retriever import retrieve
from app.agents.llm import get_llm
from langchain_core.prompts import PromptTemplate

def market_agent(state: ValidationState) -> dict:
    idea_text = state["idea_text"]
    print("\n  [1/4] Market Sizing Agent: Retrieving market evidence and estimating TAM/SAM/SOM...")
    
    # Retrieve chunks filtered to category "market-sizing"
    chunks = retrieve(query=f"market sizing for {idea_text}", top_k=5, category_filter="market-sizing")
    
    # Fallback to general corpus if nothing found
    if not chunks:
        chunks = retrieve(query=f"market sizing for {idea_text}", top_k=5)
        
    print(f"        Retrieved {len(chunks)} contextual chunk(s) from knowledge store.")
    context_text = "\n\n".join([f"Source: {c.source}\nContent: {c.text}" for c in chunks])
    
    prompt = PromptTemplate.from_template(
        """You are an expert startup analyst. Evaluate the market size for the following idea based ONLY on the provided context.
If the provided context does not contain enough information, state that explicitly and provide a best-effort qualitative estimation based on the limited context. Do not invent confident numbers without basis.

You must return your output in valid JSON format matching this EXACT schema:
{{
  "tam_estimate": "Total Addressable Market estimate string based on retrieved cases",
  "sam_estimate": "Serviceable Addressable Market estimate string based on retrieved cases",
  "som_estimate": "Serviceable Obtainable Market estimate string based on retrieved cases",
  "reasoning": "Detailed reasoning based on the retrieved cases. Note if retrieval is weak.",
  "sources": ["List of source names or citations used"]
}}

Idea: {idea_text}

Context:
{context}
"""
    )
    
    llm = get_llm()
    structured_llm = llm.with_structured_output(MarketFindings, method="json_mode")
    chain = prompt | structured_llm
    
    result = chain.invoke({"idea_text": idea_text, "context": context_text})
    
    # Ensure sources are based on actual retrieved chunks
    actual_sources = list(set([c.source for c in chunks if c.source]))
    if not result.sources:
        result.sources = actual_sources
        
    print(f"        ✓ Completed Market Sizing.")
    print(f"          • TAM: {result.tam_estimate[:80]}...")
    print(f"          • SAM: {result.sam_estimate[:80]}...")
    print(f"          • SOM: {result.som_estimate[:80]}...")
    return {"market_findings": result}
