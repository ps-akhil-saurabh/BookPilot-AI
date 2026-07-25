# BookPilot AI — Implementation Plan

## Goal

Build a production-quality **Agentic AI Reading Mentor** with 7 specialized agents, LangGraph orchestration, RAG, MCP tools, adaptive scheduling, and a premium React frontend — following all 11 project documents faithfully.

---

## Summary of Understanding

After reading all 11 documents, here is the system at a glance:

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React + Vite + TypeScript + TailwindCSS + Zustand + React Query | Premium UI with glassmorphism, agent monitors, analytics |
| Backend | FastAPI + Python 3.11 | REST API, LangGraph execution, MCP coordination |
| AI Engine | LangGraph + LangChain + Llama | Multi-agent orchestration with reflection loops |
| Database | SQLite + SQLAlchemy | 13 relational tables for books, plans, analytics, memory |
| Vector DB | ChromaDB | 4 collections for RAG (books, chapters, notes, highlights) |
| MCP | Browser, Calendar, Filesystem, Database | External tool access for agents |
| Deployment | Docker + Render | Containerized production deployment |

### 7 AI Agents
1. **Planner Agent** — Central orchestrator, intent detection, task delegation
2. **Metadata Agent** — Book info via Browser MCP (pages, genre, difficulty, ratings)
3. **Scheduling Agent** — Reading plans via Calendar MCP (daily targets, adaptive replanning)
4. **Learning Agent** — RAG-powered explanations, quizzes, flashcards via Filesystem MCP + ChromaDB
5. **Recommendation Agent** — Book suggestions via Browser MCP + long-term memory
6. **Analytics Agent** — Reading stats, streaks, predictions via Database MCP
7. **Reflection Agent** — Quality validation, triggers replanning if output is infeasible

### Core Workflow
```
User Request → Planner → [Metadata | Scheduling | Learning | Analytics | Recommendation] → Response Composer → Reflection → (Approved → END | Rejected → Planner)
```

---

## User Review Required

> [!IMPORTANT]
> **LLM Provider**: The documents specify **Llama** as the LLM. I'll integrate via `llama-cpp-python` for local inference or Ollama as a local server. Please confirm:
> - Do you have Ollama installed, or should I set up `llama-cpp-python`?
> - Which Llama model do you want to use? (e.g., `llama3.1:8b`, `llama3.2:3b`)

> [!IMPORTANT]
> **TailwindCSS Version**: The user prompt specifies TailwindCSS. I'll use **TailwindCSS v4** (latest) unless you prefer v3. Please confirm.

> [!WARNING]
> **Scope & Iteration**: This is a massive project (~18 phases, ~40+ API endpoints, 7 agents, 13 DB tables, premium UI). I will build it incrementally, phase by phase, validating each before proceeding. Each phase will produce working, testable software. The full build will span multiple conversation turns.

---

## Open Questions

> [!IMPORTANT]
> 1. **Llama Setup**: Ollama server vs. llama-cpp-python vs. cloud API (e.g., Together AI, Groq)?
> 2. **TailwindCSS**: v3 or v4?
> 3. **Embedding Model**: `all-MiniLM-L6-v2` (sentence-transformers) or a Llama-compatible embedding model?
> 4. **Docker first or local-first**: Should I set up Docker from Phase 1, or focus on local development first and add Docker later?
> 5. **Node.js version**: Do you have Node.js 18+ and Python 3.11+ installed?

---

## Proposed Changes

The project will be built in the following directory structure:

```
c:\BookPilot AI\
├── Documents/                    # (existing) Project documentation
├── backend/                      # FastAPI backend
│   ├── app/
│   │   ├── api/                  # REST controllers
│   │   ├── core/                 # Config, logging, exceptions
│   │   ├── schemas/              # Pydantic models
│   │   ├── models/               # SQLAlchemy models
│   │   ├── services/             # Business logic
│   │   ├── agents/               # AI agents (7 agents)
│   │   ├── graph/                # LangGraph (state, nodes, edges, router)
│   │   ├── rag/                  # RAG pipeline
│   │   ├── memory/               # Session + long-term memory
│   │   ├── mcp/                  # MCP tool integrations
│   │   ├── database/             # SQLite + ChromaDB + repositories
│   │   └── main.py               # FastAPI entry point
│   ├── requirements.txt
│   ├── alembic.ini
│   └── Dockerfile
├── frontend/                     # React + Vite + TypeScript
│   ├── src/
│   │   ├── components/           # Reusable UI components
│   │   ├── pages/                # Route pages
│   │   ├── hooks/                # Custom React hooks
│   │   ├── stores/               # Zustand stores
│   │   ├── services/             # API client
│   │   ├── types/                # TypeScript types
│   │   └── styles/               # Global CSS + Tailwind config
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

### Phase 1 — Project Foundation (Sprint 1)

Sets up both frontend and backend projects, folder structure, environment variables, and basic dev tooling.

#### [NEW] Backend Setup
- `backend/app/main.py` — FastAPI app with CORS, lifespan events
- `backend/app/core/config.py` — Settings via Pydantic BaseSettings
- `backend/app/core/logger.py` — Structured logging with `loguru`
- `backend/app/core/exceptions.py` — Custom exception hierarchy + handlers
- `backend/app/core/constants.py` — Application constants
- `backend/requirements.txt` — All Python dependencies
- `backend/.env.example` — Environment template

#### [NEW] Frontend Setup
- Initialize Vite + React + TypeScript project
- Configure TailwindCSS
- Set up React Router, React Query, Zustand
- Create base layout, theme system, design tokens
- `frontend/src/styles/` — CSS design system matching UI/UX doc

#### [NEW] Project Root
- `docker-compose.yml` — Backend + Frontend services
- `.gitignore` — Python, Node, IDE ignores
- `README.md` — Project overview, setup instructions
- `.env.example` — Shared environment template

---

### Phase 2 — Database & Models (Sprint 2)

#### [NEW] SQLAlchemy Models (`backend/app/models/`)
- `book.py` — Books table (id, title, author, genre, description, total_pages, language, difficulty, rating, cover_url, created_at)
- `reading.py` — reading_plans, reading_sessions, progress tables
- `learning.py` — summaries, flashcards, quizzes, vocabulary tables
- `analytics.py` — analytics, recommendations tables
- `memory.py` — memory, preferences, reflections tables

#### [NEW] Database Setup (`backend/app/database/`)
- `sqlite.py` — SQLAlchemy engine, session factory, Base
- `chromadb.py` — ChromaDB client, collection initialization
- `repositories/` — Repository classes for each entity (BookRepository, ProgressRepository, etc.)

#### [NEW] Alembic Migrations
- `alembic.ini` + `alembic/` — Database migration support

---

### Phase 3 — REST APIs (Sprint 2)

#### [NEW] Pydantic Schemas (`backend/app/schemas/`)
- `book.py` — BookCreate, BookUpdate, BookResponse
- `planner.py` — PlannerRequest, PlannerResponse
- `reading.py` — ProgressUpdate, SessionCreate
- `learning.py` — QuestionRequest, QuizResponse, FlashcardResponse
- `analytics.py` — DashboardResponse, ChartData
- `common.py` — StandardResponse wrapper

#### [NEW] API Routes (`backend/app/api/`)
- `books.py` — CRUD: POST/GET/PUT/DELETE `/api/v1/books`
- `planner.py` — POST `/api/v1/planner/generate`, `/api/v1/planner/replan`, GET `/api/v1/planner/{plan_id}`
- `reading.py` — POST `/api/v1/reading/progress`, GET `/api/v1/reading/progress/{book_id}`, GET `/api/v1/reading/history`
- `upload.py` — POST `/api/v1/upload/book`, POST `/api/v1/upload/notes`
- `learning.py` — POST `/api/v1/learning/question`, `/summary`, `/quiz`, `/flashcards`, GET `/vocabulary`
- `analytics.py` — GET `/api/v1/analytics/dashboard`, `/speed`, `/streak`, `/prediction`, `/charts`
- `recommendation.py` — GET `/api/v1/recommendation`, POST `/api/v1/recommendation/mood`
- `health.py` — GET `/api/v1/health`, `/health/ready`, `/health/live`
- `workflow.py` — POST `/api/v1/workflow/run`, GET `/api/v1/workflow/status/{id}`, GET `/api/v1/workflow/agents`
- `memory.py` — GET/PUT `/api/v1/memory`
- `reflection.py` — POST `/api/v1/reflection`, GET `/api/v1/reflection/history`

#### [NEW] Services (`backend/app/services/`)
- `book_service.py` — Book CRUD business logic
- `reading_service.py` — Progress tracking, session management
- `upload_service.py` — File processing orchestration

---

### Phase 4 — LangGraph Workflow (Sprint 3)

#### [NEW] Graph Engine (`backend/app/graph/`)
- `state.py` — `BookPilotState` TypedDict with all shared state fields
- `nodes.py` — Node functions: preprocess, planner, metadata, scheduling, learning, recommendation, analytics, compose_response, reflection
- `edges.py` — Conditional edge functions for routing
- `router.py` — Intent-based routing logic
- `graph.py` — `StateGraph` builder, compile, execution entry point

---

### Phase 5 — AI Agents (Sprint 4)

Built one at a time, in dependency order:

#### [NEW] Agents (`backend/app/agents/`)
1. `planner_agent.py` — Intent detection, task decomposition, agent selection, workflow planning
2. `metadata_agent.py` — Browser MCP invocation, metadata retrieval, difficulty estimation, caching
3. `scheduling_agent.py` — Calendar MCP, daily targets, workload balancing, deadline calculation, adaptive replanning
4. `recommendation_agent.py` — Reading order, mood analysis, genre suggestions, priority optimization
5. `analytics_agent.py` — Statistics computation, streak tracking, reading speed, completion prediction
6. `learning_agent.py` — RAG integration, explanation generation, quiz/flashcard/vocabulary creation
7. `reflection_agent.py` — Plan validation, feasibility checks, replan triggers, feedback generation

---

### Phase 6 — Memory System (Sprint 4)

#### [NEW] Memory (`backend/app/memory/`)
- `session_memory.py` — In-memory conversation context, cleared per session
- `long_term_memory.py` — SQLite-backed preferences, reading history, habits
- `summarizer.py` — Conversation summarization for context management

---

### Phase 7 — RAG Pipeline (Sprint 5)

#### [NEW] RAG (`backend/app/rag/`)
- `chunking.py` — Document chunking with overlap (PDF, EPUB, Markdown)
- `embedding.py` — Sentence-transformer embeddings generation
- `indexing.py` — ChromaDB collection management, document ingestion
- `retrieval.py` — Semantic search, top-K retrieval, context assembly

---

### Phase 8 — MCP Integrations (Sprint 6)

#### [NEW] MCP Tools (`backend/app/mcp/`)
- `browser.py` — Web scraping for book metadata (Open Library API / Google Books fallback)
- `calendar.py` — Reading availability calculation, schedule generation
- `filesystem.py` — Uploaded file access, text extraction (PyMuPDF, ebooklib)
- `database.py` — SQLite query interface for agents

Each includes: retry logic, error handling, caching, fallback behavior.

---

### Phase 9 — Frontend Core (Sprint 7)

#### [NEW] Design System
- Theme (light/dark with the indigo/cyan palette from UI doc)
- Design tokens (spacing, typography, shadows, border-radius)
- Google Fonts: Inter, Poppins, JetBrains Mono

#### [NEW] Layout & Navigation
- Floating sidebar (collapsible, animated icons)
- Top navbar (search, AI status, theme toggle)
- Responsive breakpoints (desktop, tablet, mobile)

#### [NEW] Core Pages
- **Landing Page** — Hero section, features, CTA
- **Dashboard** — Hero card, AI recommendation, progress rings, calendar, statistics, timeline, reflection card
- **Library** — Grid/list view, search, filters, upload, categories
- **Reading Plan** — Calendar view, timeline, daily tasks, adaptive schedule

---

### Phase 10 — AI & Learning Workspaces (Sprint 8)

#### [NEW] AI Workspace Page
- Chat interface with conversation panel
- Workflow visualization panel (agent execution timeline)
- Tool activity panel (MCP status indicators)
- Memory panel (preferences, history)

#### [NEW] Learning Workspace Page
- Chapter summaries
- Flashcard deck (flip animation)
- Quiz interface (MCQ, T/F, short answer)
- Vocabulary builder
- Notes
- Semantic search workspace

---

### Phase 11 — Analytics Dashboard (Sprint 9)

#### [NEW] Analytics Page
- Reading streak heatmap (GitHub-style)
- Pages per day chart (bar/line)
- Weekly reading trend
- Genre distribution (pie/donut)
- Goal completion gauge
- Reading speed graph
- Book completion timeline
- AI insights panel

---

### Phase 12 — Advanced UI Components (Sprint 9)

#### [NEW] Premium Components
- AI Thinking Timeline (step-by-step reasoning visualization)
- Agent Activity Monitor (live status cards)
- AI Confidence Meter
- Reading Heatmap
- Interactive Roadmap
- AI Reflection Console
- Smart Focus Mode
- Book DNA Visualization (radar chart)
- Dynamic Goal Predictor
- Knowledge Tree (optional — complex)

---

### Phase 13 — Reading Workspace (Sprint 8-9)

#### [NEW] Reading Session Page
- Book cover display
- Current chapter indicator
- Progress bar
- Reading timer
- Highlight button
- Ask AI button
- Session reflection form (difficulty rating, notes)
- AI sidebar (vocabulary, tips, quick summary)

---

### Phase 14 — Testing (Sprint 10)

#### Backend Tests
- Unit tests: services, repositories, utility functions
- Integration tests: API endpoints, LangGraph workflows, MCP integrations
- E2E tests: complete user journeys

#### Frontend Tests
- Component tests (React Testing Library)
- Integration tests (page-level)

---

### Phase 15 — Deployment (Sprint 10)

#### [NEW] Docker Configuration
- `backend/Dockerfile` — Python 3.11 + FastAPI + dependencies
- `frontend/Dockerfile` — Node 18 + build + nginx serve
- `docker-compose.yml` — Multi-service orchestration

#### [NEW] Render Configuration
- `render.yaml` — Service definitions
- Health check endpoints
- Environment variable configuration
- Persistent storage for SQLite + ChromaDB

---

## Verification Plan

### Automated Tests
- `cd backend && pytest` — Unit + integration tests
- `cd frontend && npm test` — Component tests
- API validation via Swagger UI at `/docs`

### Manual Verification
- Add books → verify metadata retrieval
- Create reading goal → verify plan generation with reflection
- Upload PDF → ask questions → verify RAG grounding
- Update progress → verify adaptive scheduling
- Generate quiz/flashcards → verify content relevance
- View analytics → verify chart accuracy
- Test dark mode, responsive design, accessibility
- Verify agent monitor shows real-time execution states
- Test MCP fallback behavior (disable browser → verify cached data used)

---

## Execution Strategy

I will build this project incrementally across multiple conversation turns:

| Turn | Phases | What Gets Built |
|------|--------|----------------|
| 1 | Phase 1-2 | Project setup, database models, folder structure |
| 2 | Phase 3 | All REST APIs with validation |
| 3 | Phase 4-5 | LangGraph workflow + all 7 agents |
| 4 | Phase 6-8 | Memory, RAG, MCP integrations |
| 5 | Phase 9-10 | Frontend core + AI workspace |
| 6 | Phase 11-13 | Analytics, advanced UI, reading workspace |
| 7 | Phase 14-15 | Testing + deployment |

Each turn will produce working, validated software before proceeding.
