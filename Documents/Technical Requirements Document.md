# Technical Requirements Document (TRD)

**Project Name:** BookPilot AI
**Tagline:** *An Agentic AI that plans, adapts, and guides your reading journey.*
**Version:** 1.0
**Document Type:** Technical Requirements Document (TRD)
**Date:** July 2026

---

# Table of Contents

1. Introduction
2. Technical Objectives
3. System Architecture
4. Technology Stack
5. System Components
6. Multi-Agent Architecture
7. MCP Integration
8. Retrieval-Augmented Generation (RAG)
9. Memory Architecture
10. Backend Requirements
11. Frontend Requirements
12. Database Requirements
13. Vector Database Requirements
14. API Requirements
15. LangGraph Requirements
16. Workflow Requirements
17. Performance Requirements
18. Security Considerations
19. Scalability Requirements
20. Logging & Monitoring
21. Deployment Requirements
22. Constraints
23. Future Technical Enhancements

---

# 1. Introduction

## 1.1 Purpose

This document defines the complete technical requirements for the implementation of **BookPilot AI**.

The goal is to establish a robust, modular, and extensible architecture for a **multi-agent AI application** capable of planning personalized reading schedules, retrieving knowledge from uploaded books, reasoning with external tools, and continuously improving its outputs through self-reflection.

Unlike traditional web applications, BookPilot AI combines classical backend services with AI orchestration, agent collaboration, Retrieval-Augmented Generation (RAG), and Model Context Protocol (MCP) tools.

---

# 2. Technical Objectives

The system shall:

* Support multiple specialized AI agents.
* Enable autonomous task planning and delegation.
* Integrate MCP tools for external context.
* Support Retrieval-Augmented Generation (RAG).
* Maintain both session and long-term memory.
* Execute agent workflows using LangGraph.
* Store structured and semantic data efficiently.
* Provide REST APIs for frontend integration.
* Be deployable as a containerized application on Render.

---

# 3. System Architecture

The application follows a layered architecture.

```text
+--------------------------------------------------+
|                  React Frontend                  |
+--------------------------------------------------+
                      │
                      ▼
+--------------------------------------------------+
|                FastAPI Backend                   |
+--------------------------------------------------+
                      │
                      ▼
+--------------------------------------------------+
|          LangGraph Orchestration Layer           |
+--------------------------------------------------+
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
 Planner        Specialized Agents   Reflection
                      │
                      ▼
          MCP + Memory + RAG Layer
                      │
      ┌───────────────┼───────────────┐
      ▼               ▼               ▼
 Browser MCP    Calendar MCP    Filesystem MCP
                      │
                      ▼
        SQLite + ChromaDB + Memory
```

---

# 4. Technology Stack

| Layer                | Technology                                          |
| -------------------- | --------------------------------------------------- |
| Frontend             | React                                               |
| Backend              | FastAPI                                             |
| Agent Framework      | LangGraph                                           |
| Programming Language | Python 3.11+                                        |
| LLM                  | Llama                                               |
| Database             | SQLite                                              |
| Vector Store         | ChromaDB                                            |
| Embeddings           | Sentence Transformers / Llama-compatible embeddings |
| API                  | REST                                                |
| File Processing      | PyMuPDF, pypdf, ebooklib                            |
| Background Tasks     | FastAPI Background Tasks (initially)                |
| Deployment           | Docker + Render                                     |
| Version Control      | Git + GitHub                                        |

---

# 5. System Components

## Frontend

Responsibilities:

* User interaction
* Reading dashboard
* Upload books
* Reading progress
* AI conversation interface
* Analytics visualization

---

## Backend

Responsibilities:

* API management
* LangGraph execution
* Agent orchestration
* Business logic
* Database access
* RAG pipeline
* MCP communication

---

## AI Layer

Responsibilities:

* Reasoning
* Planning
* Reflection
* Scheduling
* Recommendations
* Learning support

---

## Data Layer

Responsibilities:

* User data
* Reading history
* Metadata
* Memory
* Analytics
* Vector embeddings

---

# 6. Multi-Agent Architecture

The backend shall implement seven specialized agents.

## Planner Agent

Responsibilities:

* Understand user intent
* Decompose goals
* Create execution plan
* Delegate tasks
* Coordinate workflow

Input:

* User request

Output:

* Execution graph

---

## Metadata Agent

Responsibilities:

* Retrieve:

  * Page count
  * Genres
  * Ratings
  * Authors
  * Difficulty
  * Metadata

Uses:

* Browser MCP

---

## Scheduling Agent

Responsibilities:

* Reading targets
* Calendar optimization
* Adaptive scheduling
* Deadline estimation

Uses:

* Calendar MCP

---

## Learning Agent

Responsibilities:

* Explain paragraphs
* Generate summaries
* Flashcards
* Quizzes
* Vocabulary

Uses:

* Filesystem MCP
* ChromaDB

---

## Recommendation Agent

Responsibilities:

* Reading order
* Mood analysis
* Book recommendations
* Genre suggestions
* Priority optimization

Uses:

* Browser MCP
* Memory

---

## Analytics Agent

Responsibilities:

* Reading statistics
* Reading streak
* Reading speed
* Progress analysis
* Completion prediction

Uses:

* Database MCP

---

## Reflection Agent

Responsibilities:

Evaluate outputs before returning them.

Checks include:

* Schedule feasibility
* Reading load
* Deadline compliance
* Priority alignment
* User workload

If validation fails:

→ Return workflow to Planner Agent.

---

# 7. MCP Integration Requirements

The application shall integrate the following MCP servers.

## Browser MCP

Purpose:

Retrieve online book information.

Capabilities:

* Metadata
* Genres
* Ratings
* Difficulty
* Author details

---

## Calendar MCP

Purpose:

Determine reading availability.

Capabilities:

* Reading days
* Weekends
* Busy periods

---

## Filesystem MCP

Purpose:

Access uploaded files.

Supported formats:

* PDF
* EPUB
* Markdown

---

## Database MCP

Purpose:

Persistent storage.

Stores:

* Reading progress
* Preferences
* Analytics
* Reading history

---

# 8. Retrieval-Augmented Generation (RAG)

The application shall support semantic search over uploaded books.

Pipeline:

```text
Book Upload
      ↓
Text Extraction
      ↓
Chunking
      ↓
Embedding Generation
      ↓
ChromaDB
      ↓
Semantic Retrieval
      ↓
Context Injection
      ↓
Llama
```

Requirements:

* Support multiple uploaded books.
* Retrieve relevant chunks.
* Preserve source references where possible.
* Minimize hallucinations through grounded retrieval.

---

# 9. Memory Architecture

Two memory types shall be implemented.

## Session Memory

Purpose:

Maintain conversational context.

Examples:

* Current goal
* Selected books
* Current workflow state

Lifetime:

Current session only.

---

## Long-Term Memory

Purpose:

Persist user preferences.

Examples:

* Reading speed
* Favorite genres
* Reading habits
* Completed books
* Preferred reading time

Stored in SQLite.

---

# 10. Backend Requirements

The backend shall:

* Use FastAPI.
* Provide REST APIs.
* Manage LangGraph execution.
* Handle MCP communication.
* Manage file uploads.
* Execute RAG.
* Manage memory.
* Perform analytics.
* Return structured JSON responses.

---

# 11. Frontend Requirements

The frontend shall:

Provide:

* Dashboard
* Reading planner
* Book upload
* Chat interface
* Reading analytics
* Reading calendar
* Daily goals
* Progress tracking

Requirements:

* Responsive UI
* API integration
* Real-time updates for long-running AI tasks (polling initially; streaming can be added later)
* Clean visualization of AI reasoning (optional for MVP, desirable for transparency)

---

# 12. Database Requirements

SQLite shall store:

* Books
* Reading plans
* Reading progress
* User preferences
* Analytics
* Reading history
* Daily reflections
* Quiz results
* Vocabulary

The schema should be normalized where appropriate, while allowing efficient retrieval for analytics and planning.

---

# 13. Vector Database Requirements

ChromaDB shall store:

* Book chunks
* Embeddings
* Metadata
* Source references

Requirements:

* Semantic search
* Top-K retrieval
* Fast similarity search
* Support for multiple uploaded books

---

# 14. API Requirements

The backend shall expose REST APIs for:

### Book Management

* Upload book
* Delete book
* List books

---

### Planning

* Generate reading plan
* Update reading plan
* Recalculate schedule

---

### Learning

* Ask question
* Generate summary
* Generate flashcards
* Generate quiz

---

### Analytics

* Reading statistics
* Reading streak
* Completion forecast

---

### Progress

* Update current page
* Mark chapter complete
* Daily reflection

---

# 15. LangGraph Requirements

LangGraph shall manage:

* Agent orchestration
* State transitions
* Conditional routing
* Reflection loops
* Task delegation

The workflow shall support:

* Sequential execution
* Conditional branching
* Replanning loops
* Shared state management

---

# 16. Workflow Requirements

Typical execution flow:

1. Receive user request.
2. Planner Agent analyzes intent.
3. Required agents are selected.
4. MCP tools are invoked as needed.
5. Results are aggregated.
6. Reflection Agent validates the output.
7. If validation fails, replanning is triggered.
8. Final response is returned.

---

# 17. Performance Requirements

| Requirement                     | Target                                      |
| ------------------------------- | ------------------------------------------- |
| API response (non-AI endpoints) | < 500 ms                                    |
| AI planning response            | 5–15 seconds (depending on model and tools) |
| Metadata retrieval              | < 3 seconds (network dependent)             |
| Vector search                   | < 500 ms                                    |
| SQLite query                    | < 100 ms for typical operations             |
| File upload (10 MB PDF)         | < 5 seconds (excluding network latency)     |

The system should remain responsive while AI tasks are executing.

---

# 18. Security Considerations

Authentication is **not included** in Version 1.

However, the system shall:

* Validate uploaded file types.
* Limit upload size.
* Sanitize file names and paths.
* Prevent directory traversal in filesystem operations.
* Validate API request payloads.
* Handle malformed inputs gracefully.
* Restrict local filesystem access to approved directories.

---

# 19. Scalability Requirements

The architecture shall support future migration to:

* PostgreSQL
* Redis
* Distributed vector databases
* Additional MCP servers
* Additional AI agents
* External authentication providers
* Message queues for background processing

The design should favor loose coupling between agents and services.

---

# 20. Logging & Monitoring

The backend shall log:

* API requests
* Agent execution
* MCP tool invocations
* Reflection outcomes
* Errors and exceptions
* Workflow duration
* RAG retrieval metrics (e.g., retrieved chunks, retrieval time)

Logs should support debugging and performance analysis.

---

# 21. Deployment Requirements

Deployment target:

* Render

The application shall be packaged using Docker and include:

* FastAPI backend
* React frontend
* SQLite database (with persistent storage considerations)
* ChromaDB
* LangGraph runtime

Deployment artifacts should include:

* Dockerfile(s)
* Environment configuration
* Startup scripts
* Dependency manifests

---

# 22. Constraints

### Technical Constraints

* SQLite as the primary database.
* Llama as the LLM.
* No authentication in Version 1.
* REST API architecture.
* Docker-based deployment.
* Browser, Calendar, Filesystem, and Database MCP integration.

### Project Constraints

* Single-user focus for the initial release.
* Local file uploads only.
* English language support initially.
* Web application only (no native mobile app).

---

# 23. Future Technical Enhancements

The architecture should be designed to accommodate future capabilities without major redesign, including:

### AI Enhancements

* Streaming LLM responses
* Multi-model support
* Agent memory optimization
* Automatic prompt optimization
* Autonomous long-running workflows

### Infrastructure

* PostgreSQL
* Redis caching
* Celery or similar task queue
* Horizontal scaling
* Cloud object storage for uploaded books

### Integrations

* Google Books API
* Goodreads
* Kindle
* Google Calendar
* Email notifications
* OCR for scanned documents
* Speech-to-text and text-to-speech

---

# Technical Summary

BookPilot AI is designed as a **modular, multi-agent AI system** built on FastAPI and LangGraph. The backend orchestrates specialized agents that collaborate through shared state, leverage MCP tools for external context, use ChromaDB for retrieval-augmented generation, and maintain both session and long-term memory. The architecture prioritizes extensibility, clear separation of responsibilities, and robust AI orchestration, enabling future enhancements with minimal changes to the core design.
