from app.agents.models import ValidationState, RiskFindings
from app.retrieval.hybrid_retriever import retrieve
from app.agents.llm import get_llm
from langchain_core.prompts import PromptTemplate

def risk_agent(state: ValidationState) -> dict:
    idea_text = state["idea_text"]
    print("\n  [3/4] Risk Evaluation Agent: Analyzing multi-dimensional risk factors...")
    
    chunks = retrieve(query=f"risks challenges regulatory funding execution for {idea_text}", top_k=8)
    print(f"        Retrieved {len(chunks)} risk & regulatory chunk(s).")
    context_text = "\n\n".join([f"Source: {c.source}\nContent: {c.text}" for c in chunks])
    
    prompt = PromptTemplate.from_template(
        """You are a startup risk analyst. Evaluate the market, execution, funding, and regulatory risks for the following idea based ONLY on the provided context.
Score each risk integer from 1 to 5 (1 = lowest risk, 5 = highest risk).
In your notes, explicitly cite the specific chunks and reasons for your scores.

You must return your output in valid JSON format matching this EXACT schema:
{{
  "market_risk": 3,
  "execution_risk": 3,
  "funding_risk": 3,
  "regulatory_risk": 2,
  "notes": ["Reason for market risk citing context", "Reason for execution risk citing context", "Reason for funding risk", "Reason for regulatory risk"]
}}

Idea: {idea_text}

Context:
{context}
"""
    )
    
    llm = get_llm()
    structured_llm = llm.with_structured_output(RiskFindings, method="json_mode")
    chain = prompt | structured_llm
    
    result = chain.invoke({"idea_text": idea_text, "context": context_text})
    
    print(f"        ✓ Completed Risk Assessment:")
    print(f"          • Market Risk:      {result.market_risk}/5")
    print(f"          • Execution Risk:   {result.execution_risk}/5")
    print(f"          • Funding Risk:     {result.funding_risk}/5")
    print(f"          • Regulatory Risk:  {result.regulatory_risk}/5")
    return {"risk_findings": result}
