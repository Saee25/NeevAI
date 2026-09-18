# Neev AI - Your AI Co-Founder

Neev AI is an intelligent, multi-agent platform designed to validate and refine early-stage startup ideas. Instead of relying purely on generalized LLM knowledge, Neev AI uses a **Retrieval-Augmented Generation (RAG)** pipeline to ground its analysis in real-world historical startup case studies and verified market data.

By taking a plain-text description of a startup idea, Neev AI dynamically orchestrates a team of specialized AI agents to generate a comprehensive viability report, assess multi-dimensional risks, identify comparable startups, and even generate investor outreach drafts.

## Key Features

- **Multi-Agent Orchestration**: Built with LangGraph, the backend orchestrates a Market Agent, Competitor Agent, Risk Agent, and an Aggregator Agent that work sequentially to evaluate the startup idea.
- **Hybrid RAG Pipeline**: Combines dense vector search (`sentence-transformers`) with sparse keyword search (`BM25`) and Reciprocal Rank Fusion (RRF) to retrieve the most relevant case studies.
- **Anti-Hallucination Grounding**: Employs a strict sentence-by-sentence semantic verification step. If the final AI-generated report makes claims that are not backed up by the retrieved context, they are explicitly flagged in a "Grounding Notice" for the user.
- **Downstream Generation Tools**: Beyond the core validation report, the platform automatically generates a Pitch Outline, a Qualitative Scaling Advisor, Investor Matches, and personalized Outreach Drafts.
- **Modern, Calm UI**: A beautiful, minimalist frontend built with React, Tailwind CSS, Framer Motion (for sequential thinking animations), and Recharts (for dynamic market and risk charting).

## Major Tech Stack

### Frontend
- **Framework**: React (Vite)
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Data Visualization**: Recharts
- **Markdown**: `react-markdown` with GFM support

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **AI/LLM Framework**: LangGraph, LangChain, Groq API (Llama3/Mixtral)
- **Vector Database**: Qdrant (Local Disk Mode)
- **Embeddings & Search**: `sentence-transformers` (all-MiniLM-L6-v2), `rank_bm25`

## Datasets Used

To ensure high-quality, grounded analysis, Neev AI was seeded with specialized data:
1. **Wikipedia Narrative Case Studies**: 48 deeply factual narrative histories of prominent startup successes and failures (e.g., WeWork, Airbnb, Theranos, Stripe) extracted via Wikipedia's APIs.
2. **Kaggle Startup Metrics Dataset**: Structured data defining market trajectories, funding rounds, and operational statuses, used to ground the numerical and risk evaluations of the model.

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js & npm 

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   - Windows: `python -m venv venv` and `venv\Scripts\activate`
   - Mac/Linux: `python3 -m venv venv` and `source venv/bin/activate`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and configure your API keys (e.g., `GROQ_API_KEY`).
5. Run the server:
   *(Qdrant is configured to run locally using the file system, so no separate database container is required.)*
   ```bash
   uvicorn app.main:app --reload
   ```
6. (Optional) Run tests:
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
3. Run the development server:
   ```bash
   npm run dev
   ```

Open your browser to `http://localhost:5173` to interact with Neev AI!
