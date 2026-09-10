from .models import FinalReport, PitchOutline, InvestorMatch, OutreachDraft
from .llm import get_llm
from langchain_core.prompts import ChatPromptTemplate

class PitchOutlineAgent:
    def __init__(self):
        self.llm = get_llm().with_structured_output(PitchOutline)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert startup advisor. Your task is to reformat the provided idea validation report into a structured one-page pitch outline. Do not introduce any new claims or data not present in the report."),
            ("human", "Here is the validation report for the idea:\n\n{report_summary}\n\nMarket Findings:\n{market_findings}\n\nCompetitor Findings:\n{competitor_findings}\n\nGenerate the pitch outline.")
        ])

    def generate(self, report: FinalReport) -> PitchOutline:
        market_info = report.market_findings.json() if report.market_findings else "None"
        competitor_info = report.competitor_findings.json() if report.competitor_findings else "None"
        
        chain = self.prompt | self.llm
        return chain.invoke({
            "report_summary": report.summary,
            "market_findings": market_info,
            "competitor_findings": competitor_info
        })


class OutreachDraftAgent:
    def __init__(self):
        self.llm = get_llm().with_structured_output(OutreachDraft)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert founder writing a personalized cold email to an investor. "
                       "You have a summary of your idea and an investor match profile. "
                       "Write a short, engaging cold email referencing specific findings about the market or idea and why the investor is a good match based on their profile. "
                       "Do not use generic template filler, use the actual details provided."),
            ("human", "Idea Summary:\n{report_summary}\n\nMarket Findings:\n{market_findings}\n\nInvestor Profile:\n{investor_profile}\n\nDraft the outreach email.")
        ])

    def generate(self, report: FinalReport, investor: InvestorMatch) -> OutreachDraft:
        market_info = report.market_findings.json() if report.market_findings else "None"
        
        chain = self.prompt | self.llm
        return chain.invoke({
            "report_summary": report.summary,
            "market_findings": market_info,
            "investor_profile": investor.json()
        })
