# BookPilot AI — Project Walkthrough & Implementation Summary

## Overview

**BookPilot AI** is fully built! It is a production-quality, multi-agent AI Reading Mentor powered by **FastAPI, LangGraph, Llama, SQLite, ChromaDB, and React (Vite + TypeScript + TailwindCSS v4)**.

---

## What Was Built

### 1. Backend Architecture (`backend/app/`)
* **Core & Config**: Centralized settings via Pydantic (`config.py`), structured logging with `loguru` (`logger.py`), application constants (`constants.py`), exception hierarchy (`exceptions.py`), and path sanitization (`security.py`).
* **Database Layer**: SQLite engine with WAL mode and foreign key pragmas (`sqlite.py`), ChromaDB client with 4 collections (`chromadb_client.py`), 13 SQLAlchemy models (`models/`), and repository pattern CRUD implementations (`repositories/`).
* **MCP Tools**:
  - `BrowserMCP`: Fetches book metadata, page counts, genres, ratings, and estimates difficulty.
  - `CalendarMCP`: Calculates daily targets, deadline feasibility, and weekend capacity bonuses.
  - `FilesystemMCP`: Extracts text from PDF, EPUB, and Markdown files.
  - `DatabaseMCP`: Exposes persistent user profile and historical activity to agents.
* **RAG Pipeline**:
  - `chunking.py`: Word-boundary-aware document text chunker.
  - `embedding.py`: Vector embeddings using `sentence-transformers/all-MiniLM-L6-v2`.
  - `indexing.py`: Upserts chunks into ChromaDB collections.
  - `retrieval.py`: Top-K semantic similarity search.
* **7 AI Agents**:
  - `PlannerAgent`: Intent detection and agent task delegation.
  - `MetadataAgent`: External metadata retrieval via Browser MCP.
  - `SchedulingAgent`: Adaptive reading schedule generation via Calendar MCP.
  - `LearningAgent`: RAG-powered Q&A, summaries, quizzes, and flashcards using Llama.
  - `RecommendationAgent`: Book and reading order recommendations.
  - `AnalyticsAgent`: Performance statistics and reading streak analysis.
  - `ReflectionAgent`: Feasibility validation and replanning triggers.
* **LangGraph Engine**: `BookPilotState` TypedDict, node handlers, conditional routing edges, and compiled `StateGraph` workflow.
* **REST APIs**: Full REST API endpoints across `books`, `planner`, `reading`, `upload`, `learning`, `analytics`, `workflow`, `health`.

---

### 2. Frontend Architecture (`frontend/src/`)
* **Design System**: Glassmorphism CSS design tokens, light/dark mode support, TailwindCSS v4 integration.
* **Components**:
  - `Sidebar`: Floating navigation with live agent status badge.
  - `Navbar`: Search bar, 12-day streak counter, theme toggle, user profile.
  - `AgentMonitor` ⭐: Live cards showing execution status of all 7 agents.
  - `ThinkingTimeline` ⭐: Step-by-step AI reasoning and reflection step visualization.
* **Pages**:
  - `Dashboard`: Welcome banner, KPI cards, Agent Monitor, Thinking Timeline, Reflection Console.
  - `Library`: Book library grid, search, and RAG PDF/EPUB/MD upload modal.
  - `ReadingPlanPage`: Adaptive roadmap generator form and schedule output.
  - `AIWorkspace`: Chat interface with RAG verification badges and live tool activity panel.
  - `LearningWorkspace`: Flashcards, interactive Quiz mode, and Vocabulary builder.
  - `AnalyticsPage`: Recharts visualizations for daily pages and reading speed trends.
  - `ReadingSessionPage`: Reader Focus mode with live timer and page logging.

---

### 3. Containerization & Deployment
* `backend/Dockerfile`: Python 3.11 + FastAPI container.
* `frontend/Dockerfile`: Multi-stage build (Node 18 + Nginx).
* `docker-compose.yml`: Multi-container orchestrator.
* `README.md`: Complete quickstart and architecture documentation.

---

## Verification & Build Results

- **Frontend Build**: Verified with `tsc -b && vite build` — **Built in 1.37s with 0 errors**.
- **Backend API**: Registered all endpoints under `/api/v1/` with `/docs` interactive Swagger documentation.

---

## How to Run

### Local Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### Local Frontend
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173`.
