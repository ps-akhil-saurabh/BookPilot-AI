# LangGraph Workflow Document

**Project Name:** BookPilot AI
**Tagline:** *An Agentic AI that plans, adapts, and guides your reading journey.*
**Version:** 1.0
**Document Type:** LangGraph Workflow Document (LGWD)
**Date:** July 2026

---

# Table of Contents

1. Introduction
2. Purpose of LangGraph
3. Why LangGraph?
4. LangGraph Architecture
5. Graph Components
6. State Management
7. Workflow Execution
8. Graph Nodes
9. Conditional Routing
10. Reflection Loop
11. End-to-End Workflow
12. Individual Feature Workflows
13. Error Handling
14. Performance Optimizations
15. Future Enhancements
16. Summary

---

# 1. Introduction

## 1.1 Purpose

This document defines the **LangGraph orchestration workflow** for BookPilot AI.

LangGraph is the execution engine responsible for orchestrating the interaction between the application's specialized AI agents, shared state, MCP tools, memory, and Retrieval-Augmented Generation (RAG) pipeline.

Unlike a traditional chatbot where a single LLM handles every request, BookPilot AI uses LangGraph to coordinate multiple agents through a directed graph with conditional routing, shared state, and iterative reasoning.

---

# 2. Purpose of LangGraph

LangGraph is responsible for:

* Orchestrating all AI agents.
* Maintaining workflow state.
* Managing execution order.
* Routing requests conditionally.
* Coordinating MCP tool usage.
* Supporting replanning through reflection.
* Managing loops and retries.
* Producing the final AI response.

It acts as the **AI execution engine** of the application.

---

# 3. Why LangGraph?

Traditional AI pipelines follow a linear sequence:

```text
User → LLM → Response
```

This approach is insufficient for BookPilot AI because different user requests require different reasoning paths and external tools.

LangGraph enables:

* Stateful execution
* Multi-agent collaboration
* Dynamic routing
* Conditional execution
* Shared memory
* Reflection-based replanning
* Modular agent composition

This makes it well-suited for complex agentic workflows.

---

# 4. High-Level LangGraph Architecture

```text
                                   START
                                      │
                                      ▼
                           Request Preprocessing
                                      │
                                      ▼
                             Planner Agent
                                      │
          ┌───────────────┬───────────────┬───────────────┐
          ▼               ▼               ▼               ▼
   Metadata Node   Scheduling Node  Learning Node  Analytics Node
          │               │               │               │
          └───────────────┼───────────────┴───────────────┘
                          ▼
                 Recommendation Node
                          │
                          ▼
                  Response Composer
                          │
                          ▼
                  Reflection Node
                          │
                ┌─────────┴─────────┐
                │                   │
             Approved           Re-plan
                │                   │
                ▼                   │
               END                  │
                                    │
                                    ▼
                             Planner Agent
```

---

# 5. Graph Components

The LangGraph workflow consists of:

## Entry Node

Receives the validated request from the FastAPI backend and initializes the shared workflow state.

---

## Planner Node

Determines:

* User intent
* Required agents
* Required MCP tools
* Execution order

---

## Specialized Agent Nodes

Each agent corresponds to one or more LangGraph nodes:

* Metadata
* Scheduling
* Learning
* Recommendation
* Analytics

Each node updates the shared state with its output.

---

## Response Composer Node

Aggregates outputs from all executed agents into a coherent response structure for evaluation.

---

## Reflection Node

Evaluates the composed response against predefined criteria.

If validation fails, it routes execution back to the Planner Node.

---

## Exit Node

Returns the approved response to the backend.

---

# 6. Shared State Management

LangGraph maintains a single shared state object that is passed between nodes.

Example state:

```json
{
  "user_request": "Finish six books before September",
  "intent": "reading_plan",
  "books": [],
  "metadata": {},
  "calendar": {},
  "schedule": {},
  "recommendations": [],
  "analytics": {},
  "learning": {},
  "reflection": {},
  "response": {}
}
```

---

## State Categories

### Input State

* User request
* Uploaded files
* Current page
* Reading goal

---

### Context State

* Book metadata
* Calendar availability
* Reading speed
* User preferences
* Reading history

---

### Intermediate State

* Schedule
* Analytics
* Recommendations
* Retrieved document chunks

---

### Output State

* Final response
* Reflection result
* Updated progress

---

# 7. Workflow Execution

Every request follows the same high-level execution lifecycle.

```text
Receive Request
       │
       ▼
Initialize State
       │
       ▼
Planner Node
       │
       ▼
Determine Required Nodes
       │
       ▼
Execute Nodes
       │
       ▼
Merge Outputs
       │
       ▼
Reflection
       │
 ┌─────┴─────┐
 │           │
Valid      Invalid
 │           │
 ▼           ▼
END     Planner Node
```

---

# 8. Graph Nodes

## 8.1 Request Preprocessing Node

### Purpose

Prepare the workflow before AI execution.

### Responsibilities

* Validate input
* Normalize data
* Initialize state
* Identify uploaded resources

### Input

Backend request

### Output

Initialized graph state

---

## 8.2 Planner Node

### Purpose

Central orchestration.

### Responsibilities

* Understand intent
* Build execution strategy
* Select required agents
* Configure graph routing

### Example

Request:

> Explain Chapter 5.

Planner determines:

* Metadata ❌
* Scheduling ❌
* Learning ✅
* Recommendation ❌
* Analytics ❌

Only the Learning Node is executed.

---

## 8.3 Metadata Node

### Purpose

Retrieve external book information.

### Responsibilities

* Browser MCP calls
* Metadata caching
* Difficulty estimation

### Output

Book metadata

---

## 8.4 Scheduling Node

### Purpose

Generate or update reading schedules.

### Responsibilities

* Daily targets
* Workload balancing
* Deadline calculations
* Adaptive replanning

### Output

Reading schedule

---

## 8.5 Learning Node

### Purpose

Support learning from uploaded books.

### Responsibilities

* Retrieve relevant chunks
* Generate summaries
* Explain concepts
* Create quizzes
* Generate flashcards

### Workflow

Filesystem MCP → ChromaDB → LLM

---

## 8.6 Recommendation Node

### Purpose

Personalize reading experience.

### Responsibilities

* Reading order
* Mood-based suggestions
* Genre recommendations
* Priority optimization

---

## 8.7 Analytics Node

### Purpose

Generate insights.

### Responsibilities

* Reading streak
* Progress
* Reading speed
* Forecasts
* Statistics

---

## 8.8 Response Composer Node

### Purpose

Merge outputs from all executed nodes.

### Responsibilities

* Consolidate results
* Remove duplicates
* Format response
* Update state

---

## 8.9 Reflection Node

### Purpose

Evaluate the quality of the generated response.

### Validation Criteria

* Is the schedule feasible?
* Is the workload sustainable?
* Is the recommendation personalized?
* Is retrieved content relevant?
* Is the explanation grounded?
* Does the response satisfy the user goal?

### Output

* Approved
* Replan required
* Feedback for Planner

---

# 9. Conditional Routing

LangGraph dynamically routes execution based on user intent.

## Example 1 – Reading Plan

```text
Planner
   │
   ├── Metadata
   ├── Scheduling
   ├── Analytics
   └── Recommendation
```

Learning Node is skipped.

---

## Example 2 – Explain Paragraph

```text
Planner
   │
   └── Learning
```

Only the Learning Node executes.

---

## Example 3 – Reading Progress Update

```text
Planner
   │
   ├── Analytics
   └── Scheduling
```

Metadata and Learning Nodes are skipped.

---

# 10. Reflection Loop

The Reflection Node creates an iterative improvement cycle.

```text
Generate Response
       │
       ▼
Reflection
       │
 ┌─────┴─────┐
 │           │
Accept    Reject
 │           │
 ▼           ▼
END     Planner
             │
             ▼
      Execute Updated Plan
```

This loop ensures that responses are validated before being returned to the user.

---

# 11. End-to-End Workflow

## Scenario: Generate Reading Plan

```text
START
  │
  ▼
Preprocessing
  │
  ▼
Planner
  │
  ├── Metadata Node
  │        │
  │        ▼
  │   Browser MCP
  │
  ├── Scheduling Node
  │        │
  │        ▼
  │   Calendar MCP
  │
  ├── Analytics Node
  │        │
  │        ▼
  │   Database MCP
  │
  ├── Recommendation Node
  │
  ▼
Response Composer
  │
  ▼
Reflection
  │
 ├── Approved → END
 └── Rejected → Planner
```

---

# 12. Individual Feature Workflows

## 12.1 Book Upload

```text
START
 │
 ▼
Upload File
 │
 ▼
Filesystem MCP
 │
 ▼
Extract Text
 │
 ▼
Chunk Text
 │
 ▼
Generate Embeddings
 │
 ▼
Store in ChromaDB
 │
 ▼
END
```

---

## 12.2 Ask a Question

```text
START
 │
 ▼
Planner
 │
 ▼
Learning Node
 │
 ▼
Retrieve Chunks
 │
 ▼
LLM
 │
 ▼
Reflection
 │
 ▼
END
```

---

## 12.3 Reading Progress Update

```text
START
 │
 ▼
Planner
 │
 ▼
Analytics Node
 │
 ▼
Scheduling Node
 │
 ▼
Reflection
 │
 ▼
END
```

---

## 12.4 Daily Reminder

```text
START
 │
 ▼
Planner
 │
 ▼
Analytics
 │
 ▼
Recommendation
 │
 ▼
Response Composer
 │
 ▼
END
```

---

# 13. Error Handling

## Node Failure

If an individual node fails:

* Retry once for transient errors.
* If still unsuccessful, mark the node as unavailable.
* Continue execution if the node is optional.
* Escalate to the Planner Node if the node is mandatory.

---

## MCP Failure

* Retry MCP call.
* Use cached data if available.
* Continue with assumptions when appropriate.
* Record the assumption in the workflow state.

---

## Reflection Failure

If the Reflection Node cannot evaluate the response:

* Return the best available response.
* Mark validation status as incomplete.
* Log the incident for review.

---

# 14. Performance Optimizations

The workflow should optimize execution through:

* **Conditional execution:** Run only the nodes required for the current request.
* **Parallel execution:** Execute independent nodes (e.g., Metadata and Analytics) concurrently when there are no dependencies.
* **Caching:** Reuse metadata, embeddings, and previous retrieval results where appropriate.
* **State reuse:** Avoid recomputing unchanged information during replanning.
* **Selective retrieval:** Limit RAG searches to the most relevant document chunks.

These optimizations improve responsiveness without altering the workflow logic.

---

# 15. Future Enhancements

The LangGraph workflow is designed to evolve without significant restructuring.

Potential additions include:

* OCR Node for scanned documents.
* Notification Node for proactive reminders.
* Calendar Sync Node for external calendar integration.
* Voice Interaction Node.
* Research Node for supplementary external information.
* Multi-document comparison workflows.
* Human-in-the-loop approval nodes for advanced planning.

Because the graph is modular, these nodes can be inserted into existing workflows with minimal impact on other components.

---

# 16. Summary

LangGraph serves as the orchestration engine of BookPilot AI, coordinating specialized AI agents through a shared state and directed workflow. It enables conditional execution, iterative reflection, and modular expansion while integrating MCP tools, memory, and Retrieval-Augmented Generation into a unified execution model.

By separating planning, task execution, response composition, and validation into dedicated graph nodes, the system achieves a scalable and maintainable architecture that embodies the principles of modern Agentic AI. The workflow ensures that every user request is processed efficiently, grounded in external context where necessary, and validated before a final response is delivered.
