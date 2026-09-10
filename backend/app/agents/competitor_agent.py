from app.agents.models import ValidationState, CompetitorFindings
from app.retrieval.hybrid_retriever import retrieve
from app.agents.llm import get_llm
from langchain_core.prompts import PromptTemplate

def competitor_agent(state: ValidationState) -> dict:
    idea_text = state["idea_text"]
    
    chunks = retrieve(query=f"competitors and similar startups to {idea_text} successes and failures", top_k=8)
    context_text = "\n\n".join([f"Source: {c.source}\nURL: {c.url or 'N/A'}\nContent: {c.text}" for c in chunks])
    
    prompt = PromptTemplate.from_template(
        """You are a startup competition analyst. Identify similar startups (both successes and failures) based ONLY on the provided context.

Idea: {idea_text}

Context:
{context}
"""
    )
    
    llm = get_llm()
    structured_llm = llm.with_structured_output(CompetitorFindings)
    chain = prompt | structured_llm
    
    result = chain.invoke({"idea_text": idea_text, "context": context_text})
    
    return {"competitor_findings": result}
