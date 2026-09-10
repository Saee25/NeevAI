from langgraph.graph import StateGraph, START, END
from app.agents.models import ValidationState, FinalReport
from app.agents.market_agent import market_agent
from app.agents.competitor_agent import competitor_agent
from app.agents.risk_agent import risk_agent
from app.agents.aggregator_agent import aggregator_agent

def build_graph():
    builder = StateGraph(ValidationState)
    
    # Add nodes
    builder.add_node("market_agent", market_agent)
    builder.add_node("competitor_agent", competitor_agent)
    builder.add_node("risk_agent", risk_agent)
    builder.add_node("aggregator_agent", aggregator_agent)
    
    # Add edges sequentially for simplicity and safety
    builder.add_edge(START, "market_agent")
    builder.add_edge("market_agent", "competitor_agent")
    builder.add_edge("competitor_agent", "risk_agent")
    builder.add_edge("risk_agent", "aggregator_agent")
    builder.add_edge("aggregator_agent", END)
    
    return builder.compile()

# Singleton graph instance
app_graph = build_graph()

import time

def run_validation(idea_text: str) -> FinalReport:
    """
    Invokes the validation graph for the given startup idea text.
    """
    start_time = time.time()
    preview = idea_text.strip().replace("\n", " ")
    if len(preview) > 90:
        preview = preview[:87] + "..."
        
    print("\n" + "=" * 70)
    print("🚀 [Validation Pipeline] Starting Multi-Agent Idea Validation")
    print(f"📝 Idea: \"{preview}\"")
    print("=" * 70)
    
    initial_state = {
        "idea_text": idea_text,
        "market_findings": None,
        "competitor_findings": None,
        "risk_findings": None,
        "final_report": None
    }
    
    final_state = app_graph.invoke(initial_state)
    report = final_state["final_report"]
    
    elapsed = time.time() - start_time
    print("\n" + "=" * 70)
    print(f"✨ [Validation Pipeline] Completed in {elapsed:.2f}s | Readiness Score: {report.readiness_score}/100")
    print("=" * 70 + "\n")
    return report
