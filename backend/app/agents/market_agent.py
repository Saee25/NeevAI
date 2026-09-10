from app.agents.models import ValidationState, MarketFindings
from app.retrieval.hybrid_retriever import retrieve
from app.agents.llm import get_llm
from langchain_core.prompts import PromptTemplate

def market_agent(state: ValidationState) -> dict:
    idea_text = state["idea_text"]
    
    # Retrieve chunks filtered to category "market-sizing"
    chunks = retrieve(query=f"market sizing for {idea_text}", top_k=5, category_filter="market-sizing")
    
    # Fallback to general corpus if nothing found
    if not chunks:
        chunks = retrieve(query=f"market sizing for {idea_text}", top_k=5)
        
    context_text = "\n\n".join([f"Source: {c.source}\nContent: {c.text}" for c in chunks])
    
    prompt = PromptTemplate.from_template(
        """You are an expert startup analyst. Evaluate the market size for the following idea based ONLY on the provided context.
If the provided context does not contain enough information, state that explicitly and provide a best-effort qualitative estimation based on the limited context. Do not invent confident numbers without basis.

Idea: {idea_text}

Context:
{context}
"""
    )
    
    llm = get_llm()
    structured_llm = llm.with_structured_output(MarketFindings)
    chain = prompt | structured_llm
    
    result = chain.invoke({"idea_text": idea_text, "context": context_text})
    
    # Ensure sources are based on actual retrieved chunks
    actual_sources = list(set([c.source for c in chunks if c.source]))
    if not result.sources:
        result.sources = actual_sources
        
    return {"market_findings": result}
