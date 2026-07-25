# 🚀 BookPilot AI — Autonomous AI Reading Mentor

> An autonomous AI Reading Mentor that plans personalized reading schedules, adapts to missed sessions, explains difficult concepts, quizzes users for retention, tracks long-term progress, and continuously improves reading plans using **LangGraph, ReAct reasoning, MCP tools, RAG, Memory, and Reflection**.

---

## 🌟 Key Features

* **Multi-Agent AI Architecture**: 7 specialized agents orchestrated by LangGraph (`Planner`, `Metadata`, `Scheduling`, `Learning`, `Recommendation`, `Analytics`, `Reflection`).
* **Adaptive Scheduling & Reflection**: Automatically redistributes reading targets after missed sessions, validated by a self-reflection loop before delivery.
* **Retrieval-Augmented Generation (RAG)**: Ingest PDFs, EPUBs, and Markdown files into ChromaDB for grounded question answering.
* **MCP Integration**: Model Context Protocol servers for Browser, Calendar, Filesystem, and Database tool access.
* **Knowledge & Learning Hub**: Flashcards, quizzes with automatic scoring, and vocabulary tracking.
* **Premium Interactive UI**: Vite + React + TypeScript + TailwindCSS v4 with glassmorphism, dark mode, live agent monitors, thinking timelines, and interactive analytics charts.

---

## 🛠 Tech Stack

### Backend
* **Framework**: FastAPI (Python 3.11+)
* **AI Engine**: LangGraph + LangChain + Llama (via Cloud OpenAI-compatible API: Groq/Together/OpenRouter)
* **Database**: SQLite (SQLAlchemy 2.0)
* **Vector Store**: ChromaDB
* **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`

### Frontend
* **Core**: React 18, Vite, TypeScript
* **Styling**: TailwindCSS v4 + Glassmorphism UI
* **Icons & Charts**: Lucide React, Recharts
* **State Management**: Zustand, React Query

---

## 🚀 Quick Start (Local Development)

### 1. Backend Setup

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Add your cloud Llama API Key (e.g. Groq/Together/OpenRouter API key) to .env

uvicorn app.main:app --reload --port 8000
```
Swagger API docs available at: `http://localhost:8000/docs`

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 🐳 Running with Docker

```bash
docker-compose up --build
```

---

## 📁 Project Structure

```
BookPilot AI/
├── backend/
│   ├── app/
│   │   ├── api/          # REST controllers
│   │   ├── agents/       # 7 specialized AI agents
│   │   ├── graph/        # LangGraph state & routing engine
│   │   ├── mcp/          # Browser, Calendar, Filesystem, Database MCPs
│   │   ├── memory/       # Session & Long-term memory
│   │   ├── models/       # 13 SQLAlchemy models
│   │   ├── rag/          # Text chunking, embedding, retrieval
│   │   └── schemas/      # Pydantic schemas
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/   # AgentMonitor, ThinkingTimeline, Sidebar, Navbar
│   │   ├── pages/        # Dashboard, Library, Plan, AI Workspace, Learning, Analytics, Reader
│   │   └── services/     # API Client
```
