# Backend Schema & Workflow Document

**Project Name:** BookPilot AI
**Tagline:** *An Agentic AI that plans, adapts, and guides your reading journey.*
**Version:** 1.0
**Document Type:** Backend Schema & Workflow Document (BSWD)
**Technology Stack**

* **Framework:** FastAPI
* **Language:** Python 3.11+
* **Agent Framework:** LangGraph
* **LLM:** Llama
* **Database:** SQLite
* **Vector Database:** ChromaDB
* **Memory:** Session Memory + Long-Term Memory
* **Deployment:** Render
* **Architecture:** Planner → ReAct → Reflection → Re-plan → Response

---

# Table of Contents

1. Introduction
2. Backend Goals
3. High-Level Backend Architecture
4. Folder Structure
5. Backend Layers
6. Complete Request Lifecycle
7. Backend Workflow
8. Service Responsibilities
9. LangGraph Integration
10. Memory Management
11. RAG Workflow
12. MCP Integration
13. API Processing Pipeline
14. Background Jobs
15. Caching Strategy
16. Logging & Monitoring
17. Exception Handling
18. Backend State Flow
19. Future Scalability
20. Summary

---

# 1. Introduction

The backend of BookPilot AI is the **intelligence layer** of the application.

Unlike a conventional CRUD backend, BookPilot AI coordinates multiple AI agents, retrieval systems, memory layers, and external tools through LangGraph.

The backend is responsible for:

* Business logic
* AI orchestration
* Agent execution
* Tool invocation
* State management
* Retrieval
* Data persistence
* Analytics
* Response generation

The frontend never communicates directly with AI components. All interactions pass through the backend.

---

# 2. Backend Goals

The backend should:

* Be modular
* Be scalable
* Support multiple AI agents
* Handle long-running AI workflows
* Support reflection loops
* Provide reusable services
* Maintain conversation state
* Support future authentication
* Be cloud deployable
* Expose REST APIs

---

# 3. High-Level Backend Architecture

```text
                   React Frontend
                          │
                          ▼
                 FastAPI REST API
                          │
         ┌────────────────┼─────────────────┐
         ▼                ▼                 ▼
 Controller Layer    Service Layer     AI Layer
         │                │                 │
         └────────────────┼─────────────────┘
                          ▼
                 LangGraph Engine
                          │
        ┌─────────────────┼───────────────────┐
        ▼                 ▼                   ▼
 Planner Agent     Specialized Agents   Reflection Agent
        │
        ▼
 MCP Tools + Memory + RAG
        │
        ▼
 SQLite + ChromaDB
```

---

# 4. Recommended Folder Structure

```text
backend/
│
├── app/
│   ├── api/
│   │    ├── books.py
│   │    ├── planner.py
│   │    ├── reading.py
│   │    ├── analytics.py
│   │    ├── learning.py
│   │    ├── recommendation.py
│   │    └── upload.py
│   │
│   ├── core/
│   │    ├── config.py
│   │    ├── constants.py
│   │    ├── logger.py
│   │    ├── exceptions.py
│   │    └── security.py
│   │
│   ├── schemas/
│   │    ├── book.py
│   │    ├── planner.py
│   │    ├── analytics.py
│   │    └── user.py
│   │
│   ├── models/
│   │    ├── book.py
│   │    ├── reading.py
│   │    ├── quiz.py
│   │    └── analytics.py
│   │
│   ├── services/
│   │    ├── metadata_service.py
│   │    ├── scheduling_service.py
│   │    ├── rag_service.py
│   │    ├── analytics_service.py
│   │    ├── recommendation_service.py
│   │    └── memory_service.py
│   │
│   ├── agents/
│   │    ├── planner_agent.py
│   │    ├── metadata_agent.py
│   │    ├── scheduling_agent.py
│   │    ├── learning_agent.py
│   │    ├── analytics_agent.py
│   │    ├── recommendation_agent.py
│   │    └── reflection_agent.py
│   │
│   ├── graph/
│   │    ├── graph.py
│   │    ├── state.py
│   │    ├── router.py
│   │    ├── nodes.py
│   │    └── edges.py
│   │
│   ├── rag/
│   │    ├── embedding.py
│   │    ├── retrieval.py
│   │    ├── chunking.py
│   │    └── indexing.py
│   │
│   ├── memory/
│   │    ├── session_memory.py
│   │    ├── long_term_memory.py
│   │    └── summarizer.py
│   │
│   ├── mcp/
│   │    ├── browser.py
│   │    ├── calendar.py
│   │    ├── filesystem.py
│   │    └── database.py
│   │
│   ├── database/
│   │    ├── sqlite.py
│   │    ├── chromadb.py
│   │    └── repositories/
│   │
│   └── main.py
│
└── requirements.txt
```

---

# 5. Backend Layers

## Presentation Layer

Responsible for:

* REST APIs
* Request validation
* Response serialization

Components:

* FastAPI
* Pydantic

---

## Business Logic Layer

Responsible for:

* Reading logic
* Analytics
* Planning
* Recommendations
* Scheduling

---

## Agent Layer

Responsible for:

* AI reasoning
* ReAct workflow
* Reflection
* Delegation

---

## Data Layer

Responsible for:

* SQLite
* ChromaDB
* Memory

---

## Integration Layer

Responsible for:

* Browser MCP
* Calendar MCP
* Filesystem MCP
* Database MCP

---

# 6. Complete Request Lifecycle

Example:

User requests:

> I want to finish these books before September.

Workflow:

```text
Frontend

↓

FastAPI

↓

Validate Request

↓

Planner API

↓

LangGraph

↓

Planner Agent

↓

Metadata Agent

↓

Browser MCP

↓

Scheduling Agent

↓

Calendar MCP

↓

Analytics Agent

↓

Reflection Agent

↓

Generate Response

↓

Frontend
```

---

# 7. Backend Workflow

## Step 1

Receive Request

↓

Validate

↓

Create Request Context

↓

Initialize Graph State

---

## Step 2

Planner Agent

↓

Identify Intent

↓

Determine Required Agents

↓

Create Execution Plan

---

## Step 3

Execute Agents

Each agent updates shared state.

Example:

Metadata Agent

↓

Scheduling Agent

↓

Recommendation Agent

↓

Analytics Agent

---

## Step 4

Reflection

↓

Evaluate Output

↓

Need Re-plan?

↓

Yes

↓

Planner

↓

Repeat

---

## Step 5

Compose Final Response

↓

Store Updates

↓

Return JSON

---

# 8. Service Responsibilities

## Metadata Service

Responsibilities

* Browser MCP calls
* Metadata cache
* Difficulty estimation

---

## Scheduling Service

Responsibilities

* Reading plans
* Adaptive scheduling
* Deadline calculations

---

## Analytics Service

Responsibilities

* Reading statistics
* Progress
* Predictions

---

## Recommendation Service

Responsibilities

* Book ranking
* Mood analysis
* Priority optimization

---

## RAG Service

Responsibilities

* Embedding generation
* Retrieval
* Similarity search

---

## Memory Service

Responsibilities

* Session context
* Long-term preferences
* Summaries

---

# 9. LangGraph Integration

```text
Request

↓

Graph Initialization

↓

Planner

↓

Conditional Routing

↓

Agent Execution

↓

Response Merge

↓

Reflection

↓

END
```

Every request passes through LangGraph.

No business logic should bypass the graph for AI-related tasks.

---

# 10. Memory Management

Two memory layers are maintained.

## Session Memory

Stores:

* Current conversation
* Current books
* Temporary context

Expires after session ends.

---

## Long-Term Memory

Stores:

* Favorite genres
* Reading speed
* Reading habits
* Preferred difficulty
* Reading goals

Persists indefinitely.

---

Memory Flow

```text
User

↓

Planner

↓

Memory Service

↓

Retrieve Context

↓

Agents

↓

Update Memory
```

---

# 11. RAG Workflow

When users upload books:

```text
Upload

↓

Extract Text

↓

Chunk

↓

Embedding

↓

ChromaDB
```

When asking questions:

```text
Question

↓

Embedding

↓

Similarity Search

↓

Relevant Chunks

↓

LLM

↓

Answer
```

---

# 12. MCP Integration

### Browser MCP

* Metadata
* Authors
* Ratings

---

### Calendar MCP

* Reading availability
* Reading schedule

---

### Filesystem MCP

* PDFs
* EPUBs
* Markdown

---

### Database MCP

* Reading history
* Analytics
* Preferences

---

# 13. API Processing Pipeline

```text
Receive Request

↓

Middleware

↓

Validation

↓

Controller

↓

Service

↓

LangGraph

↓

Agents

↓

Reflection

↓

Formatter

↓

Response
```

---

# 14. Background Jobs

The backend should support asynchronous tasks for operations that may take significant time.

Examples include:

* PDF text extraction
* Document chunking
* Embedding generation
* ChromaDB indexing
* Metadata prefetching
* Analytics recalculation
* Memory summarization
* Scheduled reminder generation

These jobs can be handled using FastAPI background tasks initially and migrated to a dedicated task queue (e.g., Celery or Dramatiq) as the application scales.

---

# 15. Caching Strategy

To improve performance and reduce redundant processing:

### Metadata Cache

* Store retrieved book metadata locally.
* Refresh periodically or on demand.

### Embedding Cache

* Avoid regenerating embeddings for unchanged documents.

### Retrieval Cache

* Cache frequently accessed document chunks.

### Planning Cache

* Reuse existing plans when user goals have not changed significantly.

### Analytics Cache

* Cache aggregated metrics and invalidate after progress updates.

---

# 16. Logging & Monitoring

The backend should produce structured logs for observability.

### Log Categories

* API requests
* Agent execution
* LangGraph transitions
* MCP tool calls
* Database queries
* Errors and exceptions
* Performance metrics

### Metrics to Monitor

* API latency
* Agent execution time
* Reflection loop frequency
* MCP success/failure rate
* RAG retrieval latency
* ChromaDB query performance

Integration with monitoring tools (e.g., Prometheus and Grafana) can be added in future versions.

---

# 17. Exception Handling

The backend should implement centralized exception handling.

### Validation Errors

* Return HTTP 422 with descriptive validation messages.

### Business Logic Errors

* Return appropriate HTTP status codes (400/409) with actionable feedback.

### Agent Errors

* Retry transient failures.
* Log persistent failures.
* Continue execution where possible.

### MCP Errors

* Retry once.
* Fall back to cached or default values if available.

### Database Errors

* Roll back failed transactions.
* Return generic user-facing messages while logging detailed diagnostics.

### RAG Errors

* Fall back to direct LLM responses when retrieval is unavailable.
* Clearly indicate when responses are not grounded in uploaded content.

---

# 18. Backend State Flow

The backend maintains a shared workflow state throughout each request.

```text
Request Received
        │
        ▼
State Initialized
        │
        ▼
Context Loaded
        │
        ▼
Planner Execution
        │
        ▼
Agent Updates
        │
        ▼
Reflection
        │
   ┌────┴────┐
   │         │
Approved   Re-plan
   │         │
   ▼         ▼
Response   Planner
```

The state object contains:

* User request
* Intent
* Selected books
* Metadata
* Schedule
* Recommendations
* Analytics
* Learning outputs
* Reflection status
* Final response

---

# 19. Future Scalability

The backend architecture is designed to evolve as BookPilot AI grows.

### Planned Enhancements

* PostgreSQL support for production deployments.
* Redis for distributed caching and session storage.
* Dedicated background workers (Celery/Dramatiq).
* WebSocket support for streaming AI responses and live agent progress.
* Horizontal scaling of FastAPI instances behind a load balancer.
* Separate microservices for AI orchestration, RAG, and analytics.
* Authentication and user management.
* Multi-tenant architecture.
* Event-driven communication using message brokers (RabbitMQ/Kafka).

The modular separation of controllers, services, agents, and integrations ensures that these enhancements can be introduced without major refactoring.

---

# 20. Summary

The backend of **BookPilot AI** is designed as an intelligent orchestration layer rather than a traditional REST service. FastAPI provides the API surface, while LangGraph coordinates specialized AI agents through a shared state. These agents leverage MCP tools, session and long-term memory, Retrieval-Augmented Generation, and persistent storage to generate personalized, explainable, and adaptive reading experiences.

By organizing the backend into clear architectural layers—presentation, business logic, agent orchestration, integration, and data persistence—the system remains modular, maintainable, and extensible. This design not only supports the current feature set but also provides a robust foundation for future enhancements such as real-time collaboration, streaming responses, additional AI agents, and cloud-native scaling.
