# API Specification Document (ASD)

**Project Name:** BookPilot AI
**Tagline:** *An Agentic AI that plans, adapts, and guides your reading journey.*
**Version:** 1.0
**Document Type:** API Specification Document (ASD)
**API Style:** RESTful API
**Backend Framework:** FastAPI
**Response Format:** JSON
**Authentication:** None (v1)
**Date:** July 2026

---

# Table of Contents

1. Introduction
2. API Design Principles
3. API Architecture
4. Request Lifecycle
5. Standard Response Format
6. Error Handling
7. API Modules
8. Complete Endpoint Specifications
9. AI Agent APIs
10. Learning APIs
11. Analytics APIs
12. Memory APIs
13. MCP APIs
14. Health APIs
15. HTTP Status Codes
16. API Versioning
17. Future APIs

---

# 1. Introduction

## Purpose

This document defines all REST APIs exposed by the BookPilot AI backend.

The APIs provide access to:

* Reading library
* AI planning
* Reading schedules
* Learning assistant
* Analytics
* Recommendations
* Memory
* AI workflow
* Reflection
* RAG

The frontend communicates **only** with these APIs.

No frontend component directly accesses:

* LangGraph
* SQLite
* ChromaDB
* MCP Tools

---

# 2. API Design Principles

The APIs follow these principles:

* RESTful
* Stateless
* JSON only
* Predictable URLs
* Consistent response format
* Proper HTTP methods
* Idempotent where applicable
* Modular grouping
* Easy future versioning

---

# 3. API Architecture

```text
React Frontend

↓

REST APIs

↓

FastAPI Controllers

↓

Services

↓

LangGraph

↓

Agents

↓

SQLite / ChromaDB / MCP
```

---

# 4. Request Lifecycle

```text
Client Request

↓

Middleware

↓

Validation

↓

Controller

↓

Business Service

↓

LangGraph

↓

Agent Execution

↓

Reflection

↓

JSON Response
```

---

# 5. Standard Response Format

## Success Response

```json
{
  "success": true,
  "message": "Operation completed successfully.",
  "data": {},
  "timestamp": "2026-07-20T10:30:00Z"
}
```

---

## Error Response

```json
{
  "success": false,
  "message": "Book not found.",
  "error": {
    "code": "BOOK_NOT_FOUND",
    "details": "No book exists with ID 12."
  },
  "timestamp": "2026-07-20T10:30:00Z"
}
```

---

# 6. Error Handling

| HTTP Code | Meaning               |
| --------- | --------------------- |
| 200       | Success               |
| 201       | Resource Created      |
| 204       | No Content            |
| 400       | Bad Request           |
| 404       | Resource Not Found    |
| 409       | Conflict              |
| 422       | Validation Error      |
| 429       | Rate Limit            |
| 500       | Internal Server Error |
| 503       | Service Unavailable   |

---

# 7. API Modules

```text
/api/v1

├── books
├── planner
├── schedule
├── reading
├── upload
├── learning
├── analytics
├── recommendation
├── memory
├── reflection
├── workflow
├── mcp
└── health
```

---

# 8. Complete Endpoint Specifications

---

# Books API

---

## 1. Add Book

**POST**

```text
/api/v1/books
```

### Description

Add a new book to the library.

### Request

```json
{
  "title": "Atomic Habits",
  "author": "James Clear",
  "genre": "Self Help",
  "pages": 320
}
```

### Response

```json
{
  "book_id": 1,
  "message": "Book added successfully."
}
```

---

## 2. Get All Books

**GET**

```text
/api/v1/books
```

### Response

```json
[
  {
    "id": 1,
    "title": "Atomic Habits",
    "progress": 35
  }
]
```

---

## 3. Get Book Details

**GET**

```text
/api/v1/books/{book_id}
```

---

## 4. Update Book

**PUT**

```text
/api/v1/books/{book_id}
```

---

## 5. Delete Book

**DELETE**

```text
/api/v1/books/{book_id}
```

---

# Planner API

---

## Generate Reading Plan

**POST**

```text
/api/v1/planner/generate
```

### Description

Invokes LangGraph Planner Agent to generate a personalized reading plan.

### Request

```json
{
  "deadline": "2026-09-01",
  "daily_minutes": 45,
  "book_ids": [1,2,3]
}
```

### Response

```json
{
  "plan_id": 21,
  "estimated_days": 41,
  "daily_pages": 26,
  "confidence": 0.94
}
```

---

## Replan Reading Schedule

**POST**

```text
/api/v1/planner/replan
```

### Request

```json
{
  "plan_id": 21,
  "missed_days": 2
}
```

---

## Get Current Plan

**GET**

```text
/api/v1/planner/{plan_id}
```

---

# Schedule API

---

## Today's Reading

**GET**

```text
/api/v1/schedule/today
```

### Response

```json
{
  "pages": 22,
  "estimated_minutes": 35,
  "book": "Atomic Habits"
}
```

---

## Weekly Schedule

**GET**

```text
/api/v1/schedule/week
```

---

## Monthly Timeline

**GET**

```text
/api/v1/schedule/month
```

---

# Reading Progress API

---

## Update Reading Progress

**POST**

```text
/api/v1/reading/progress
```

### Request

```json
{
  "book_id":1,
  "current_page":120,
  "minutes":40
}
```

### Processing

* Update progress
* Update analytics
* Trigger Reflection Agent
* Update schedule if required

---

## Get Reading Progress

**GET**

```text
/api/v1/reading/progress/{book_id}
```

---

## Reading History

**GET**

```text
/api/v1/reading/history
```

---

# Upload API

---

## Upload Book

**POST**

```text
/api/v1/upload/book
```

### Multipart

```text
file=AtomicHabits.pdf
```

### Processing

```text
Upload

↓

Extract Text

↓

Chunk

↓

Embedding

↓

Store ChromaDB
```

---

## Upload Notes

**POST**

```text
/api/v1/upload/notes
```

---

# Learning API

---

## Ask Question

**POST**

```text
/api/v1/learning/question
```

### Request

```json
{
  "book_id":1,
  "question":"Explain habit stacking."
}
```

### Processing

```text
Retrieve

↓

RAG

↓

LLM

↓

Answer
```

---

## Generate Summary

**POST**

```text
/api/v1/learning/summary
```

---

## Generate Quiz

**POST**

```text
/api/v1/learning/quiz
```

### Response

```json
{
  "questions":[]
}
```

---

## Generate Flashcards

**POST**

```text
/api/v1/learning/flashcards
```

---

## Vocabulary

**GET**

```text
/api/v1/learning/vocabulary
```

---

# Recommendation API

---

## Get Recommendation

**GET**

```text
/api/v1/recommendation
```

### Response

```json
{
  "recommended_book":"Atomic Habits",
  "reason":"Easy reading after technical books.",
  "confidence":0.91
}
```

---

## Mood Recommendation

**POST**

```text
/api/v1/recommendation/mood
```

### Request

```json
{
  "mood":"tired"
}
```

---

# Analytics API

---

## Dashboard

**GET**

```text
/api/v1/analytics/dashboard
```

### Response

```json
{
  "books":12,
  "completed":8,
  "streak":25,
  "speed":28
}
```

---

## Reading Speed

**GET**

```text
/api/v1/analytics/speed
```

---

## Reading Streak

**GET**

```text
/api/v1/analytics/streak
```

---

## Goal Prediction

**GET**

```text
/api/v1/analytics/prediction
```

---

## Charts

**GET**

```text
/api/v1/analytics/charts
```

Returns aggregated data for:

* Reading heatmap
* Weekly trend
* Genre distribution
* Completion timeline
* Reading speed

---

# Memory API

---

## Retrieve Memory

**GET**

```text
/api/v1/memory
```

Returns:

* Preferences
* Reading habits
* Favorite genres

---

## Update Memory

**PUT**

```text
/api/v1/memory
```

---

# Reflection API

---

## Evaluate Plan

**POST**

```text
/api/v1/reflection
```

### Response

```json
{
  "approved":true,
  "feedback":[]
}
```

---

## Reflection History

**GET**

```text
/api/v1/reflection/history
```

---

# Workflow API

---

## Graph Execution

**POST**

```text
/api/v1/workflow/run
```

Runs complete LangGraph workflow.

---

## Workflow Status

**GET**

```text
/api/v1/workflow/status/{workflow_id}
```

Returns:

```json
{
  "planner":"completed",
  "metadata":"completed",
  "learning":"running",
  "reflection":"pending"
}
```

---

## Agent Activity

**GET**

```text
/api/v1/workflow/agents
```

Returns live agent execution states for the UI's Agent Activity Monitor.

---

# MCP API

These endpoints act as internal abstractions over MCP tool interactions. They may be hidden from public clients in production.

---

## Browser Metadata

**POST**

```text
/api/v1/mcp/browser/metadata
```

---

## Calendar Availability

**GET**

```text
/api/v1/mcp/calendar
```

---

## Filesystem Search

**POST**

```text
/api/v1/mcp/filesystem/search
```

---

## Database Query

**POST**

```text
/api/v1/mcp/database/query
```

---

# Health API

---

## Health Check

**GET**

```text
/api/v1/health
```

### Response

```json
{
  "status":"healthy",
  "database":"connected",
  "chromadb":"connected",
  "llm":"available",
  "langgraph":"running"
}
```

---

## Readiness Check

**GET**

```text
/api/v1/health/ready
```

Verifies that all required dependencies are initialized before serving traffic.

---

## Liveness Check

**GET**

```text
/api/v1/health/live
```

Confirms that the backend process is alive.

---

# 15. HTTP Status Codes

| Status                    | Usage                                               |
| ------------------------- | --------------------------------------------------- |
| 200 OK                    | Successful GET, PUT, POST operations returning data |
| 201 Created               | New resource successfully created                   |
| 202 Accepted              | Long-running background job accepted                |
| 204 No Content            | Successful DELETE or empty response                 |
| 400 Bad Request           | Invalid business request                            |
| 401 Unauthorized          | Reserved for future authentication                  |
| 403 Forbidden             | Reserved for future authorization                   |
| 404 Not Found             | Resource does not exist                             |
| 409 Conflict              | Duplicate or conflicting resource                   |
| 422 Unprocessable Entity  | Validation failure                                  |
| 429 Too Many Requests     | Rate limiting                                       |
| 500 Internal Server Error | Unexpected server failure                           |
| 503 Service Unavailable   | External dependency unavailable                     |

---

# 16. API Versioning

The API uses URI-based versioning.

```text
/api/v1/...
```

Future releases may introduce:

```text
/api/v2/...
```

Versioning ensures backward compatibility while allowing the introduction of new features or breaking changes.

---

# 17. Future APIs

The following endpoints are planned for future releases:

### Authentication

* `POST /api/v1/auth/login`
* `POST /api/v1/auth/logout`
* `POST /api/v1/auth/register`

### Notifications

* Reading reminders
* Push notifications
* Email summaries

### Collaboration

* Shared reading groups
* Group challenges
* Discussion threads

### Voice AI

* Voice reading companion
* Speech-to-text notes
* Audio summaries

### Calendar Sync

* Google Calendar integration
* Outlook Calendar integration

### External Book Services

* Goodreads synchronization
* Kindle progress import
* Open Library metadata synchronization

### AI Streaming

* Server-Sent Events (SSE) or WebSocket endpoints for streaming AI responses.
* Live LangGraph node execution updates.
* Real-time reflection status.

---

# API Module Summary

| Module         | Primary Responsibility                                               |
| -------------- | -------------------------------------------------------------------- |
| Books          | Library management                                                   |
| Planner        | AI reading plan generation and replanning                            |
| Schedule       | Daily, weekly, and monthly reading schedules                         |
| Reading        | Progress tracking and reading history                                |
| Upload         | Book and notes ingestion                                             |
| Learning       | RAG-powered explanations, summaries, quizzes, flashcards, vocabulary |
| Recommendation | Personalized reading suggestions                                     |
| Analytics      | Reading statistics, predictions, and charts                          |
| Memory         | Long-term preferences and personalization                            |
| Reflection     | Plan evaluation and validation                                       |
| Workflow       | LangGraph execution and agent status                                 |
| MCP            | Internal access to Browser, Calendar, Filesystem, and Database tools |
| Health         | Service health, readiness, and liveness checks                       |

---

# Summary

The BookPilot AI API is designed around a modular, agent-driven architecture where FastAPI serves as the gateway to LangGraph-powered workflows. Each API module encapsulates a distinct business capability, while shared response formats, standardized error handling, and clear versioning ensure consistency and maintainability.

This specification supports the application's current functionality—including adaptive reading plans, AI-assisted learning, analytics, memory, and Retrieval-Augmented Generation—while providing a clear path for future enhancements such as authentication, real-time streaming, collaboration, and third-party integrations. The resulting API surface is scalable, developer-friendly, and well aligned with the overall Agentic AI architecture of BookPilot AI.
