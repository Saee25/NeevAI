# Neev AI

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js & npm (Required for the frontend)

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Copy `.env.example` to `.env` and fill in your API keys.
6. Start local Qdrant via Docker:
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```
7. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
8. Run tests:
   ```bash
   python -m pytest tests/
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the dev server:
   ```bash
   npm run dev
   ```

## Current Progress

- **Section 1: Project Initialization**: Base FastAPI backend and React frontend structure.
- **Section 2: Data Ingestion Pipeline**: Corpus chunking, preprocessing, and glossary extraction setup.
- **Section 3: Hybrid Retrieval Layer**: Implemented Qdrant dense vector search (via `sentence-transformers`) and sparse search (`rank_bm25`) combined with Reciprocal Rank Fusion (RRF).
- **Section 4: Core Validation Agents (LangGraph Orchestrator)**: Implemented Market, Risk, and Competitor analysis agents using LangGraph for multi-step execution.
- **Section 5: Downstream Generation Agents**: Added Pitch Outline generation, Investor Matching using `sentence-transformers` semantic matching, and personalized Outreach Draft generation.
- **Section 6: Scaling Advisor Agent**: Implemented `ScalingAgent` to provide qualitative scaling guidance based on retrieved case studies without making direct numeric recommendations.
- **Section 7: API Finalization**: Wired routers into `main.py`, added CORS, `slowapi` rate limiting (5 req/min for validate, 10 req/min for generate), global error handling, simple in-memory caching for validation, health endpoint, and comprehensive pytest coverage using mocked LLM responses.
- **Section 8: Frontend Design System & Layout**: Set up Tailwind CSS with custom design tokens (cream, sage, charcoal), configured typography (Fraunces, Inter), and built a clean, calm, minimal hero landing page layout and a reusable Card component.
- **Section 9: Agent Reveal Animation & Results Display**: Implemented frontend React components for presenting validation results. Built `AgentReveal` for sequential Framer Motion thinking animations, `ReadinessScore` for a circular animated SVG score, Recharts-powered `MarketChart` and `RiskRadar`, a clean `CompetitorList`, and an interactive `GlossaryTooltip` with custom dotted styling. Wired these into the main application view with a mockup state.
- **Section 10: Downstream Feature Components**: Built downstream views and horizontal tab navigation in `App.jsx`. Added `PitchOutline` for clean presentation, `InvestorMatches` for displaying investor data, `OutreachDraft` with an editable text area and copy functionality, `ScalingAdvisor` for the secondary revenue scaling flow, and an exportable `ReportCard` component powered by `html-to-image`.
