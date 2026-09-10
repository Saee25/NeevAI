from langgraph.graph import StateGraph, START, END
from backend.app.agents.models import ValidationState, FinalReport
from backend.app.agents.market_agent import market_agent
from backend.app.agents.competitor_agent import competitor_agent
from backend.app.agents.risk_agent import risk_agent
from backend.app.agents.aggregator_agent import aggregator_agent

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

def run_validation(idea_text: str) -> FinalReport:
    """
    Invokes the validation graph for the given startup idea text.
    """
    initial_state = {
        "idea_text": idea_text,
        "market_findings": None,
        "competitor_findings": None,
        "risk_findings": None,
        "final_report": None
    }
    
    final_state = app_graph.invoke(initial_state)
    return final_state["final_report"]
