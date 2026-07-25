# MCP Tools & Workflow Document

**Project Name:** BookPilot AI
**Tagline:** *An Agentic AI that plans, adapts, and guides your reading journey.*
**Version:** 1.0
**Document Type:** MCP Tools & Workflow Document
**Date:** July 2026

---

# Table of Contents

1. Introduction
2. What is MCP?
3. Why MCP is Used in BookPilot AI
4. MCP Architecture
5. MCP Components
6. MCP Servers Used
7. MCP Workflow
8. MCP Tool Responsibilities
9. Agent-to-MCP Interaction
10. Complete Workflow Examples
11. MCP State Management
12. MCP Error Handling
13. Security Considerations
14. Future MCP Integrations
15. Summary

---

# 1. Introduction

## 1.1 Purpose

This document describes how **Model Context Protocol (MCP)** is integrated into BookPilot AI to enable AI agents to interact with external tools and data sources.

BookPilot AI is not designed as a standalone Large Language Model (LLM). Instead, it functions as an **Agentic AI system** where specialized agents retrieve real-world information through MCP servers before reasoning and generating responses.

By integrating MCP, the system gains access to:

* Book metadata
* User schedules
* Uploaded documents
* Reading history
* Persistent storage

This allows agents to make informed decisions rather than relying solely on the LLM's internal knowledge.

---

# 2. What is MCP?

**Model Context Protocol (MCP)** is a standardized communication protocol that enables AI agents to interact with external tools, services, databases, and applications in a structured manner.

Instead of embedding all knowledge within the LLM, MCP allows the model to:

* Retrieve external information.
* Read and write structured data.
* Access files.
* Query databases.
* Interact with calendars.
* Perform actions using external systems.

Within BookPilot AI, MCP acts as the bridge between the AI agents and the external resources required for planning and learning.

---

# 3. Why MCP is Used in BookPilot AI

Traditional LLMs have limitations:

* They may not know the latest book metadata.
* They cannot access a user's uploaded books directly.
* They cannot inspect a user's reading progress stored in a database.
* They cannot calculate schedules based on calendar availability without external context.

MCP addresses these limitations by enabling agents to fetch real-time or user-specific information before making decisions.

This results in:

* More accurate planning.
* Personalized recommendations.
* Grounded explanations.
* Dynamic schedule generation.
* Better user experience.

---

# 4. MCP Architecture

The following architecture illustrates how MCP integrates with the multi-agent system.

```text
                        User
                          │
                          ▼
                 Planner Agent
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
 Metadata Agent    Scheduling Agent   Learning Agent
        │                 │                 │
        ▼                 ▼                 ▼
 Browser MCP      Calendar MCP     Filesystem MCP
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ▼
                    Database MCP
                          │
                          ▼
                  SQLite / ChromaDB
```

The Planner Agent does not interact with MCP directly. Instead, it delegates requests to specialized agents, which invoke the appropriate MCP server.

---

# 5. MCP Components

BookPilot AI consists of four MCP servers, each responsible for a specific category of external information.

| MCP Server     | Primary Purpose                           |
| -------------- | ----------------------------------------- |
| Browser MCP    | Retrieve online book metadata             |
| Calendar MCP   | Manage reading schedules and availability |
| Filesystem MCP | Access uploaded books and notes           |
| Database MCP   | Read and update persistent user data      |

Each MCP server exposes a set of tools that agents invoke when required.

---

# 6. MCP Servers Used

## 6.1 Browser MCP

### Purpose

Provides access to publicly available book information.

### Responsibilities

* Retrieve page count.
* Retrieve author information.
* Retrieve publication details.
* Retrieve genres.
* Retrieve ratings.
* Estimate reading difficulty.
* Retrieve book summaries (if available).

### Used By

* Metadata Agent
* Recommendation Agent

### Example Request

**Input**

```text
Book: Clean Code
```

**Browser MCP Response**

```text
Title: Clean Code
Author: Robert C. Martin
Pages: 464
Genre: Software Engineering
Difficulty: Medium
Rating: 4.7
```

---

## 6.2 Calendar MCP

### Purpose

Provides scheduling information to build personalized reading plans.

### Responsibilities

* Determine available reading days.
* Identify weekends.
* Identify busy periods.
* Estimate reading capacity.
* Support adaptive scheduling.

### Used By

* Scheduling Agent

### Example

User Availability

```text
Monday-Friday

45 minutes/day

Saturday

2 hours

Sunday

Rest
```

Calendar MCP returns structured availability, which the Scheduling Agent converts into a reading plan.

---

## 6.3 Filesystem MCP

### Purpose

Provides access to user-uploaded learning resources.

### Supported Files

* PDF
* EPUB
* Markdown

### Responsibilities

* Read uploaded books.
* Extract text.
* Access notes.
* Read highlights.
* Supply content to the RAG pipeline.

### Used By

* Learning Agent

### Example

User asks:

> Explain Chapter 3.

Filesystem MCP locates the uploaded document, extracts the relevant text, and passes it to the RAG pipeline for retrieval and explanation.

---

## 6.4 Database MCP

### Purpose

Provides access to persistent application data.

### Responsibilities

* Store reading progress.
* Retrieve reading history.
* Update daily progress.
* Store user preferences.
* Retrieve analytics.
* Store reflections.
* Maintain reading streaks.

### Used By

* Analytics Agent
* Scheduling Agent
* Recommendation Agent

### Example

Retrieve:

* Current page: 145
* Reading speed: 28 pages/hour
* Streak: 12 days

---

# 7. MCP Workflow

Every user request follows a structured workflow.

## Step 1 – User Request

Example:

> I want to finish six books before September.

The Planner Agent analyzes the request and identifies the required information.

---

## Step 2 – Agent Delegation

The Planner Agent determines which specialized agents are required.

For this request:

* Metadata Agent
* Scheduling Agent
* Analytics Agent
* Recommendation Agent

---

## Step 3 – MCP Invocation

Each agent invokes its required MCP server.

```text
Metadata Agent
       │
       ▼
 Browser MCP

Scheduling Agent
       │
       ▼
 Calendar MCP

Analytics Agent
       │
       ▼
 Database MCP
```

---

## Step 4 – Context Collection

Each MCP server returns structured information.

Example:

Browser MCP

* Page count
* Genre
* Difficulty

Calendar MCP

* Reading availability

Database MCP

* Reading speed
* Previous books

---

## Step 5 – Planning

The Planner Agent combines all retrieved information and generates an execution plan.

---

## Step 6 – Reflection

The Reflection Agent evaluates the generated schedule.

Questions include:

* Is the workload realistic?
* Can the deadline be met?
* Is the reading order appropriate?

---

## Step 7 – Response

If approved:

Return the reading plan.

If rejected:

Return the workflow to the Planner Agent for replanning.

---

# 8. MCP Tool Responsibilities

| MCP Tool       | Responsibilities                                  |
| -------------- | ------------------------------------------------- |
| Browser MCP    | Retrieve metadata and book information            |
| Calendar MCP   | Retrieve user availability and scheduling context |
| Filesystem MCP | Read uploaded documents and notes                 |
| Database MCP   | Store and retrieve persistent application data    |

---

# 9. Agent-to-MCP Interaction

| Agent                | Browser          | Calendar | Filesystem | Database    |
| -------------------- | ---------------- | -------- | ---------- | ----------- |
| Planner Agent        | No               | No       | No         | Read Memory |
| Metadata Agent       | Yes              | No       | No         | No          |
| Scheduling Agent     | No               | Yes      | No         | Read        |
| Learning Agent       | No               | No       | Yes        | Read        |
| Recommendation Agent | Yes              | No       | No         | Read        |
| Analytics Agent      | No               | No       | No         | Read/Write  |
| Reflection Agent     | Read (if needed) | Read     | Read       | Read        |

The Planner Agent coordinates workflow but does not directly invoke external tools.

---

# 10. Complete Workflow Examples

## Scenario 1 – Reading Plan Generation

### User Request

> I have four books and want to finish them before August 30.

### Workflow

```text
User
  │
  ▼
Planner Agent
  │
  ├── Metadata Agent
  │       │
  │       ▼
  │   Browser MCP
  │
  ├── Scheduling Agent
  │       │
  │       ▼
  │   Calendar MCP
  │
  ├── Analytics Agent
  │       │
  │       ▼
  │   Database MCP
  │
  ├── Recommendation Agent
  │       │
  │       ▼
  │   Browser MCP + Database MCP
  │
  ▼
Reflection Agent
  │
  ├── Valid → Final Reading Plan
  └── Invalid → Planner Agent
```

---

## Scenario 2 – Explain a Paragraph

### User Request

> Explain this paragraph from Chapter 5.

### Workflow

```text
User
  │
  ▼
Planner Agent
  │
  ▼
Learning Agent
  │
  ▼
Filesystem MCP
  │
  ▼
Extract Book Content
  │
  ▼
ChromaDB Retrieval
  │
  ▼
Llama
  │
  ▼
Reflection Agent
  │
  ▼
Explanation Returned
```

---

## Scenario 3 – User Misses Reading Sessions

### User

> I missed reading for the last three days.

### Workflow

```text
Planner Agent
      │
      ▼
Analytics Agent
      │
      ▼
Database MCP
      │
      ▼
Retrieve Progress
      │
      ▼
Scheduling Agent
      │
      ▼
Calendar MCP
      │
      ▼
Generate Updated Schedule
      │
      ▼
Reflection Agent
      │
      ▼
Updated Reading Plan
```

---

# 11. MCP State Management

Each MCP interaction updates the shared workflow state.

Example state object:

```json
{
  "goal": "Finish books before September",
  "books": [
    {
      "title": "Atomic Habits",
      "pages": 320,
      "difficulty": "Easy"
    }
  ],
  "availability": {
    "weekday_minutes": 45,
    "weekend_minutes": 120
  },
  "reading_speed": 28,
  "schedule": {
    "daily_target": 18
  },
  "reflection": {
    "status": "Approved"
  }
}
```

This shared state allows all agents to work with consistent information throughout the workflow.

---

# 12. MCP Error Handling

### Browser MCP Failure

Fallback:

* Retry request.
* Use cached metadata if available.
* Ask the user to provide missing details.

---

### Calendar MCP Failure

Fallback:

* Assume a default daily reading duration.
* Mark the schedule as based on estimated availability.

---

### Filesystem MCP Failure

Fallback:

* Verify the uploaded file exists.
* Request the user to re-upload the file if necessary.

---

### Database MCP Failure

Fallback:

* Continue with session data if available.
* Skip analytics that require historical data.
* Notify the Planner Agent of limited personalization.

---

### General Principles

* Retry transient failures.
* Log all tool failures.
* Avoid terminating the workflow when partial information is sufficient.
* Clearly communicate assumptions made due to missing data.

---

# 13. Security Considerations

Although Version 1 does not include user authentication, MCP interactions must follow secure practices:

* Restrict Filesystem MCP to approved directories.
* Validate uploaded file types and sizes.
* Sanitize file paths to prevent directory traversal.
* Validate all data exchanged with MCP servers.
* Handle malformed responses gracefully.
* Avoid exposing internal server details in user-facing messages.

---

# 14. Future MCP Integrations

The architecture supports additional MCP servers that can be integrated with minimal changes to the Planner Agent.

Potential future integrations include:

| MCP Server          | Purpose                               |
| ------------------- | ------------------------------------- |
| Google Books MCP    | Richer metadata and previews          |
| Goodreads MCP       | Import reading lists and reviews      |
| Google Calendar MCP | Synchronize real calendars            |
| Notification MCP    | Email and push reminders              |
| OCR MCP             | Extract text from scanned books       |
| Speech MCP          | Voice interaction and read-aloud      |
| Cloud Storage MCP   | Access books stored in cloud services |

Each new MCP server would expose specialized tools that can be invoked by existing or newly introduced agents.

---

# 15. Summary

The Model Context Protocol (MCP) layer is a foundational component of BookPilot AI. It enables specialized agents to access reliable external information instead of relying solely on the LLM's internal knowledge. By separating tool access into dedicated MCP servers for browser, calendar, filesystem, and database operations, the system achieves modularity, transparency, and extensibility.

Combined with the Planner Agent, LangGraph orchestration, RAG, and the Reflection Agent, MCP ensures that every reading plan, recommendation, explanation, and analytics report is grounded in current, user-specific, and verifiable context. This architecture exemplifies modern Agentic AI design by combining autonomous reasoning with structured tool usage.
