from app.agents.models import ValidationState, CompetitorFindings
from app.retrieval.hybrid_retriever import retrieve
from app.agents.llm import get_llm
from langchain_core.prompts import PromptTemplate

def competitor_agent(state: ValidationState) -> dict:
    idea_text = state["idea_text"]
    print("\n  [2/4] Competitor Analyst Agent: Scanning competitor landscape & outcomes...")
    
    chunks = retrieve(query=f"competitors and similar startups to {idea_text} successes and failures", top_k=8)
    print(f"        Retrieved {len(chunks)} case study chunk(s).")
    context_text = "\n\n".join([f"Source: {c.source}\nURL: {c.url or 'N/A'}\nContent: {c.text}" for c in chunks])
    
    prompt = PromptTemplate.from_template(
        """You are a startup competition analyst. Identify similar startups (both successes and failures) based ONLY on the provided context.

You must return your output in valid JSON format matching this EXACT schema:
{{
  "similar_startups": [
    {{
      "name": "Startup Name",
      "outcome": "Success, Failure, or Current status",
      "summary": "Summary of what they did, trajectory, and outcome",
      "source_url": "URL or citation source"
    }}
  ],
  "positioning_notes": "Strategic positioning notes and market differentiation analysis"
}}

Idea: {idea_text}

Context:
{context}
"""
    )
    
    llm = get_llm()
    structured_llm = llm.with_structured_output(CompetitorFindings, method="json_mode")
    chain = prompt | structured_llm
    
    result = chain.invoke({"idea_text": idea_text, "context": context_text})
    
    print(f"        ✓ Completed Competitor Analysis: Found {len(result.similar_startups)} comparable startup(s).")
    for s in result.similar_startups[:3]:
        print(f"          • {s.name} ({s.outcome}): {s.summary[:60]}...")
    return {"competitor_findings": result}
