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
6. Run the server:
   ```bash
   uvicorn app.main:app --reload
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
