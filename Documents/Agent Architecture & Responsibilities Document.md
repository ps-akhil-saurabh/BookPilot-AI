# Agent Architecture & Responsibilities Document (AARD)

**Project Name:** BookPilot AI
**Tagline:** *An Agentic AI that plans, adapts, and guides your reading journey.*
**Version:** 1.0
**Document Type:** Agent Architecture & Responsibilities Document (AARD)
**Date:** July 2026

---

# Table of Contents

1. Introduction
2. Purpose of Multi-Agent Architecture
3. High-Level Agent Architecture
4. Agent Communication Model
5. Shared Workflow State
6. Agent Execution Lifecycle
7. Planner Agent
8. Metadata Agent
9. Scheduling Agent
10. Learning Agent
11. Recommendation Agent
12. Analytics Agent
13. Reflection Agent
14. Agent Interaction Sequence
15. Agent State Management
16. Agent-to-MCP Mapping
17. LangGraph Node Mapping
18. Error Handling & Recovery
19. Future Agent Expansion
20. Agent Design Principles

---

# 1. Introduction

## 1.1 Purpose

This document defines the architecture, responsibilities, communication patterns, lifecycle, and interactions of the AI agents that make up the **BookPilot AI** system.

Unlike conventional AI applications where a single LLM performs every task, BookPilot AI follows a **multi-agent architecture**, where each agent specializes in one domain and collaborates with others under the supervision of a central orchestrator.

This design improves:

* Modularity
* Maintainability
* Explainability
* Scalability
* Extensibility
* Separation of concerns

---

# 2. Why Multi-Agent Architecture?

A single AI model can answer questions, but it often mixes planning, retrieval, scheduling, reasoning, and validation into one prompt. This makes the system difficult to debug, extend, and control.

BookPilot AI instead divides responsibilities among specialized agents, allowing each agent to focus on a well-defined task.

### Benefits

* Clear separation of responsibilities
* Independent agent development and testing
* Easier prompt engineering
* Better scalability
* Easier integration of new capabilities
* Improved transparency of reasoning
* Reflection before response generation

---

# 3. High-Level Agent Architecture

```text
                              USER
                                │
                                ▼
                    Planner Agent (Brain)
                                │
        ┌──────────────┬──────────────┬──────────────┐
        ▼              ▼              ▼              ▼
 Metadata Agent  Scheduling Agent  Learning Agent  Analytics Agent
        │              │              │              │
        └──────────────┼──────────────┴──────────────┘
                       ▼
             Recommendation Agent
                       │
                       ▼
               Reflection Agent
                       │
             ┌─────────┴─────────┐
             │                   │
          Accepted          Needs Revision
             │                   │
             ▼                   ▼
      Final Response      Planner Agent
```

---

# 4. Agent Communication Model

The system follows a centralized orchestration model.

* The **Planner Agent** is the only agent that receives the initial user request.
* Other agents do not communicate directly with each other.
* All communication flows through the Planner Agent using a shared workflow state.

This avoids circular dependencies and keeps execution predictable.

### Communication Flow

```text
User
 │
 ▼
Planner
 │
 ├── Metadata
 ├── Scheduling
 ├── Learning
 ├── Recommendation
 ├── Analytics
 │
 ▼
Reflection
 │
 ├── Approved → Final Response
 └── Rejected → Planner
```

---

# 5. Shared Workflow State

All agents operate on a common workflow state managed by LangGraph.

The shared state includes:

* User request
* User goals
* Uploaded books
* Reading history
* Metadata
* Calendar information
* Intermediate results
* Reading plan
* Reflection feedback
* Final response

Each agent reads only the information it requires and writes back its outputs.

---

# 6. Agent Execution Lifecycle

```text
User Request
      │
      ▼
Planner Activated
      │
Create Execution Plan
      │
Delegate Tasks
      │
Collect Results
      │
Reflection
      │
Valid?
 │         │
Yes        No
 │          │
 ▼          ▼
Return    Re-plan
```

---

# 7. Planner Agent

## Purpose

The Planner Agent is the central orchestrator and decision-maker of the system. It is responsible for understanding user intent, creating an execution strategy, coordinating other agents, and assembling the final response.

## Responsibilities

* Interpret user requests.
* Identify the primary objective.
* Detect missing information.
* Break complex requests into subtasks.
* Determine which agents are required.
* Execute the workflow.
* Merge outputs from all agents.
* Send results for reflection.
* Trigger replanning if necessary.
* Produce the final response.

## Inputs

* User request
* Session memory
* Long-term memory
* Previous workflow state

## Outputs

* Execution plan
* Agent task list
* Consolidated response
* Updated workflow state

## Tools

The Planner Agent does **not** call MCP tools directly. It delegates those responsibilities to specialized agents.

## Example

**User Request**

> "I want to finish six books before September."

The Planner Agent identifies:

* Metadata is required.
* Calendar availability is required.
* Reading schedule is required.
* Recommendations are beneficial.
* Analytics can estimate feasibility.

It delegates these tasks to the appropriate agents.

---

# 8. Metadata Agent

## Purpose

The Metadata Agent gathers all information related to books.

## Responsibilities

* Retrieve page counts.
* Identify genres.
* Retrieve author details.
* Determine publication details.
* Fetch ratings.
* Estimate reading difficulty.
* Cache metadata for future use.

## Inputs

* Book title
* ISBN (if available)
* Existing metadata cache

## Outputs

* Complete book metadata
* Difficulty estimate

## MCP Usage

Uses **Browser MCP**.

## Example

Input:

> "Atomic Habits"

Output:

* Pages: 320
* Genre: Self-help
* Author: James Clear
* Difficulty: Easy
* Rating: 4.8

---

# 9. Scheduling Agent

## Purpose

The Scheduling Agent creates realistic reading schedules based on user availability and goals.

## Responsibilities

* Calculate reading duration.
* Estimate pages per day.
* Create daily reading plans.
* Balance workload.
* Adjust plans after missed sessions.
* Predict completion dates.

## Inputs

* Metadata
* Calendar availability
* Reading speed
* Deadline

## Outputs

* Personalized reading schedule
* Daily targets
* Completion estimate

## MCP Usage

Uses **Calendar MCP**.

## Example

Input:

* 320-page book
* 45 minutes/day
* Deadline in 30 days

Output:

* 12 pages/day
* Finish by target date

---

# 10. Learning Agent

## Purpose

The Learning Agent improves comprehension and retention by interacting with uploaded book content.

## Responsibilities

* Explain paragraphs.
* Summarize chapters.
* Generate quizzes.
* Create flashcards.
* Extract key points.
* Build vocabulary lists.
* Answer questions about uploaded books.

## Inputs

* User questions
* Uploaded books
* Retrieved context

## Outputs

* Explanations
* Summaries
* Quizzes
* Flashcards
* Vocabulary

## MCP Usage

Uses:

* Filesystem MCP
* ChromaDB (RAG)

## Example

User:

> "Explain this chapter."

The agent:

1. Retrieves relevant text from ChromaDB.
2. Builds context.
3. Generates an explanation grounded in the uploaded content.

---

# 11. Recommendation Agent

## Purpose

The Recommendation Agent optimizes the user's reading journey by suggesting books, reading order, and priorities.

## Responsibilities

* Recommend books.
* Suggest reading order.
* Analyze user mood.
* Recommend genres.
* Optimize priorities.
* Personalize suggestions.

## Inputs

* Reading history
* User preferences
* Metadata
* Current goals

## Outputs

* Reading recommendations
* Reading order
* Personalized suggestions

## MCP Usage

Uses:

* Browser MCP
* Long-term memory

## Example

User:

> "I'm tired today."

Recommendation:

Read **Atomic Habits** instead of **Deep Learning**.

---

# 12. Analytics Agent

## Purpose

The Analytics Agent tracks user performance and generates insights.

## Responsibilities

* Reading streak calculation.
* Reading speed estimation.
* Progress tracking.
* Reading statistics.
* Goal prediction.
* Visualization data.

## Inputs

* Reading history
* Daily progress
* User activity

## Outputs

* Reading analytics
* Completion predictions
* Charts
* Performance summaries

## MCP Usage

Uses **Database MCP**.

## Example

Output:

* Reading streak: 18 days
* Average speed: 28 pages/hour
* Completion probability: 92%

---

# 13. Reflection Agent

## Purpose

The Reflection Agent is the quality assurance layer of the multi-agent system. It evaluates the generated output before it is returned to the user.

## Responsibilities

* Validate feasibility.
* Detect unrealistic schedules.
* Identify excessive workload.
* Verify deadlines.
* Check recommendation quality.
* Request replanning when necessary.

## Evaluation Questions

* Is the schedule realistic?
* Is the workload sustainable?
* Does the plan meet the deadline?
* Are priorities respected?
* Is the reading order appropriate?
* Has the user's reading history been considered?
* Are difficult books distributed appropriately?

## Inputs

* Complete workflow state
* Reading plan
* Recommendations
* Analytics

## Outputs

* Approval
* Revision request
* Feedback for Planner Agent

## Example

Generated schedule:

75 pages/day

Reflection:

Average user speed:

25 pages/day

Decision:

Reject plan.

Feedback:

Reduce daily workload and extend schedule if possible.

---

# 14. Agent Interaction Sequence

```text
User
 │
 ▼
Planner
 │
 ▼
Metadata
 │
 ▼
Planner
 │
 ▼
Scheduling
 │
 ▼
Learning (if required)
 │
 ▼
Recommendation
 │
 ▼
Analytics
 │
 ▼
Reflection
 │
 ├── Valid → Final Response
 └── Invalid → Planner
```

---

# 15. Agent State Management

Each agent maintains only the state required for its responsibilities.

| Agent          | State Maintained                                     |
| -------------- | ---------------------------------------------------- |
| Planner        | Current goal, execution plan, pending tasks          |
| Metadata       | Metadata cache, difficulty estimates                 |
| Scheduling     | Reading schedule, daily targets                      |
| Learning       | Retrieved document chunks, generated study materials |
| Recommendation | Preference model, suggested reading order            |
| Analytics      | Reading metrics, streaks, progress                   |
| Reflection     | Validation results, revision feedback                |

Shared workflow state enables collaboration while keeping agents loosely coupled.

---

# 16. Agent-to-MCP Mapping

| Agent          | Browser MCP      | Calendar MCP | Filesystem MCP | Database MCP  | ChromaDB        |
| -------------- | ---------------- | ------------ | -------------- | ------------- | --------------- |
| Planner        | No               | No           | No             | Read (Memory) | No              |
| Metadata       | Yes              | No           | No             | No            | No              |
| Scheduling     | No               | Yes          | No             | Read          | No              |
| Learning       | No               | No           | Yes            | Read          | Yes             |
| Recommendation | Yes              | No           | No             | Read          | Read (optional) |
| Analytics      | No               | No           | No             | Yes           | No              |
| Reflection     | Read (if needed) | Read         | Read           | Read          | Read            |

---

# 17. LangGraph Node Mapping

Each agent maps directly to one or more LangGraph nodes.

```text
START
  │
  ▼
Planner
  │
  ├── Metadata
  ├── Scheduling
  ├── Learning (conditional)
  ├── Recommendation (conditional)
  ├── Analytics
  │
  ▼
Reflection
  │
  ├── Approved → END
  └── Rejected → Planner
```

Conditional execution ensures that only the necessary agents run for a given request.

---

# 18. Error Handling & Recovery

### Metadata Retrieval Failure

* Retry Browser MCP.
* Fall back to cached metadata.
* Ask the user for missing details if required.

### Calendar Unavailable

* Assume a default daily reading availability.
* Notify the Planner Agent that the schedule is based on assumptions.

### Learning Agent Failure

* Retry retrieval from ChromaDB.
* If retrieval fails, explain that the requested content could not be located.

### Analytics Failure

* Generate insights using available progress data.
* Mark advanced metrics as unavailable.

### Reflection Failure

* Return the best available plan with a note that validation could not be completed.
* Log the incident for review.

---

# 19. Future Agent Expansion

The architecture is designed to support additional specialized agents without changing the core orchestration model.

Possible future agents include:

* **OCR Agent** – Extract text from scanned books.
* **Voice Agent** – Voice interaction and read-aloud features.
* **Calendar Sync Agent** – Google Calendar integration.
* **Notification Agent** – Email and reminder management.
* **Goodreads Agent** – Import reading lists and reviews.
* **Google Books Agent** – Enhanced metadata retrieval.
* **Research Agent** – Supplement book content with external references.

New agents can be added as independent LangGraph nodes and invoked by the Planner Agent when required.

---

# 20. Agent Design Principles

The following principles guide the design of all agents in BookPilot AI:

* **Single Responsibility:** Each agent focuses on one well-defined domain.
* **Loose Coupling:** Agents communicate through shared workflow state rather than direct dependencies.
* **Centralized Orchestration:** The Planner Agent coordinates all workflows.
* **Tool Specialization:** MCP tools are accessed only by the agents responsible for their domain.
* **Shared Context:** Relevant information is exchanged through a common state managed by LangGraph.
* **Validation Before Delivery:** Every workflow passes through the Reflection Agent before a response is returned.
* **Extensibility:** New agents can be introduced without redesigning the existing architecture.

---

# Conclusion

The multi-agent architecture of **BookPilot AI** transforms a conventional AI assistant into a coordinated ecosystem of specialized agents. Each agent contributes domain-specific expertise while the Planner Agent orchestrates execution and the Reflection Agent ensures quality through iterative validation. This architecture provides a scalable foundation for autonomous reasoning, transparent decision-making, and future expansion, making BookPilot AI a robust demonstration of modern Agentic AI principles.
