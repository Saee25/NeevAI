import re
from app.agents.models import ValidationState, FinalReport
from app.retrieval.hybrid_retriever import retrieve
from app.retrieval.embeddings import embed_texts
from app.agents.llm import get_llm
from langchain_core.prompts import PromptTemplate

def compute_similarity(vec1, vec2):
    return sum(a * b for a, b in zip(vec1, vec2))

def aggregator_agent(state: ValidationState) -> dict:
    idea_text = state["idea_text"]
    market = state.get("market_findings")
    competitor = state.get("competitor_findings")
    risk = state.get("risk_findings")
    
    print("\n  [4/4] Aggregator & Grounding Agent: Synthesizing report & scoring readiness...")
    
    # 1. Synthesize summary using LLM
    prompt = PromptTemplate.from_template(
        """You are a startup co-founder AI. Write a comprehensive, concise summary report for the following startup idea, 
incorporating the provided market, competitor, and risk findings. Do not invent any new numbers or facts. 

Idea: {idea_text}

Market Findings: {market}
Competitor Findings: {competitor}
Risk Findings: {risk}
"""
    )
    
    llm = get_llm()
    summary_chain = prompt | llm
    summary_result = summary_chain.invoke({
        "idea_text": idea_text,
        "market": market.model_dump_json() if market else "N/A",
        "competitor": competitor.model_dump_json() if competitor else "N/A",
        "risk": risk.model_dump_json() if risk else "N/A"
    })
    
    summary_text = summary_result.content
    print("        ✓ Synthesized startup report summary.")
    
    # 2. Calculate explicit Founder Readiness Score (0-100)
    # Weights: market 30%, competition 25%, risk 25%, clarity of idea 20%
    market_score = 0
    if market and "not enough" not in market.tam_estimate.lower():
        market_score = 30
    elif market:
        market_score = 15

    competitor_score = 0
    if competitor and competitor.similar_startups:
        competitor_score = min(25, len(competitor.similar_startups) * 5 + 10)
        
    risk_score = 25
    if risk:
        avg_risk = (risk.market_risk + risk.execution_risk + risk.funding_risk + risk.regulatory_risk) / 4.0
        risk_score = max(0, int(25 - ((avg_risk - 1) * (25/4))))
        
    clarity_score = min(20, len(idea_text.split()) // 2)
    
    readiness_score = min(100, market_score + competitor_score + risk_score + clarity_score)
    print(f"        ✓ Founder Readiness Score computed: {int(readiness_score)}/100")
    print(f"          (Market: {market_score}/30, Comp: {competitor_score}/25, Risk: {risk_score}/25, Clarity: {clarity_score}/20)")
    
    # 3. Groundedness Check
    # Retrieve chunks again to act as our grounding corpus
    m_chunks = retrieve(query=f"market sizing for {idea_text}", top_k=5)
    c_chunks = retrieve(query=f"competitors and similar startups to {idea_text} successes and failures", top_k=5)
    r_chunks = retrieve(query=f"risks challenges regulatory funding execution for {idea_text}", top_k=5)
    
    all_chunks = m_chunks + c_chunks + r_chunks
    chunk_texts = list(set([c.text for c in all_chunks]))
    
    sentences = re.split(r'(?<=[.!?]) +', summary_text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    
    unverified_claims = []
    if chunk_texts and sentences:
        chunk_embeddings = embed_texts(chunk_texts)
        sentence_embeddings = embed_texts(sentences)
        
        threshold = 0.60 # Cosine similarity threshold for NLI/overlap proxy
        
        for i, sent_emb in enumerate(sentence_embeddings):
            if chunk_embeddings:
                max_sim = max(compute_similarity(sent_emb, c_emb) for c_emb in chunk_embeddings)
                if max_sim < threshold:
                    unverified_claims.append(sentences[i])
            else:
                unverified_claims.append(sentences[i])
                
    print(f"        ✓ Grounding check complete: {len(unverified_claims)} unverified claim(s) flagged.")
    
    report = FinalReport(
        readiness_score=int(readiness_score),
        summary=summary_text,
        market_findings=market,
        competitor_findings=competitor,
        risk_findings=risk,
        unverified_claims=unverified_claims
    )
    
    return {"final_report": report}
