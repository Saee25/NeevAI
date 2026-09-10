from backend.app.agents.models import ValidationState, RiskFindings
from backend.app.retrieval.hybrid_retriever import retrieve
from backend.app.agents.llm import get_llm
from langchain_core.prompts import PromptTemplate

def risk_agent(state: ValidationState) -> dict:
    idea_text = state["idea_text"]
    
    chunks = retrieve(query=f"risks challenges regulatory funding execution for {idea_text}", top_k=8)
    context_text = "\n\n".join([f"Source: {c.source}\nContent: {c.text}" for c in chunks])
    
    prompt = PromptTemplate.from_template(
        """You are a startup risk analyst. Evaluate the market, execution, funding, and regulatory risks for the following idea based ONLY on the provided context.
Score each risk from 1 to 5 (1 = lowest risk, 5 = highest risk).
In your notes, explicitly cite the specific chunks and reasons for your scores.

Idea: {idea_text}

Context:
{context}
"""
    )
    
    llm = get_llm()
    structured_llm = llm.with_structured_output(RiskFindings)
    chain = prompt | structured_llm
    
    result = chain.invoke({"idea_text": idea_text, "context": context_text})
    
    return {"risk_findings": result}
