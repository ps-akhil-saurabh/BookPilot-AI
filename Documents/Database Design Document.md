# Database Design Document (DDD)

**Project Name:** BookPilot AI
**Tagline:** *An Agentic AI that plans, adapts, and guides your reading journey.*
**Version:** 1.0
**Document Type:** Database Design Document (DDD)
**Database:** SQLite (Primary) + ChromaDB (Vector Database)
**ORM:** SQLAlchemy
**Migration Tool:** Alembic *(recommended for future upgrades)*
**Date:** July 2026

---

# Table of Contents

1. Introduction
2. Database Objectives
3. Database Architecture
4. Database Technologies
5. High-Level Database Schema
6. Relational Database Design
7. Entity Relationship Diagram (ERD)
8. Table Specifications
9. ChromaDB Design
10. Long-Term Memory Design
11. Session Memory Design
12. Data Relationships
13. Database Workflows
14. Indexing Strategy
15. Constraints & Validation
16. Backup & Recovery
17. Future Scalability
18. Summary

---

# 1. Introduction

## Purpose

This document defines the complete database architecture for **BookPilot AI**.

Unlike a traditional CRUD application, BookPilot AI stores multiple types of information:

* User reading library
* Reading plans
* Reading progress
* AI-generated summaries
* Flashcards
* Quizzes
* Reading analytics
* Long-term memory
* Reflection history
* Vector embeddings for Retrieval-Augmented Generation (RAG)

To support these requirements, the system uses a hybrid storage model:

* **SQLite** for structured relational data.
* **ChromaDB** for semantic search and vector embeddings.

---

# 2. Database Objectives

The database is designed to:

* Store all application data persistently.
* Support AI agent workflows.
* Enable adaptive scheduling.
* Track reading progress.
* Maintain long-term user preferences.
* Store AI-generated learning artifacts.
* Provide fast retrieval for analytics.
* Support semantic search through vector storage.
* Be easy to migrate to PostgreSQL in future versions.

---

# 3. Database Architecture

```text
                   BookPilot AI

                         │

        ┌────────────────┴────────────────┐

        ▼                                 ▼

     SQLite                         ChromaDB

(Relational Data)               (Vector Storage)

        │                                 │

        ▼                                 ▼

Books                    Book Embeddings

Progress                 Chapter Embeddings

Reading Plans            Semantic Chunks

Analytics                Notes Embeddings

Preferences              Highlights
```

---

# 4. Database Technologies

## Primary Database

SQLite

Stores:

* Structured relational data
* Reading history
* Analytics
* Preferences
* Plans
* Learning artifacts

---

## Vector Database

ChromaDB

Stores:

* Book embeddings
* Chapter embeddings
* Semantic chunks
* Notes
* Highlights

---

## ORM

SQLAlchemy

Responsible for:

* Object mapping
* Relationships
* Queries
* Transactions

---

# 5. High-Level Database Schema

```text
User (Virtual)
      │
      ├──────────────┐
      ▼              ▼

Books          User Preferences

      │

      ▼

Reading Plans

      │

      ▼

Reading Sessions

      │

      ▼

Analytics

      │

      ▼

Learning

 ├── Summaries

 ├── Flashcards

 ├── Quiz

 ├── Vocabulary

 └── Reflections
```

> **Note:** Version 1 of BookPilot AI does not implement authentication. The "User" entity is represented as a virtual profile to keep the schema ready for future multi-user support.

---

# 6. Relational Database Design

The SQLite database consists of the following primary tables:

| Table            | Purpose                         |
| ---------------- | ------------------------------- |
| books            | Store book metadata             |
| reading_plans    | Personalized AI-generated plans |
| reading_sessions | Daily reading activity          |
| progress         | Reading progress                |
| recommendations  | AI recommendations              |
| analytics        | Computed statistics             |
| summaries        | AI summaries                    |
| quizzes          | Generated quizzes               |
| flashcards       | Generated flashcards            |
| vocabulary       | Learned vocabulary              |
| reflections      | Daily learning reflections      |
| preferences      | Long-term preferences           |
| memory           | Long-term AI memory             |

---

# 7. Entity Relationship Diagram (ERD)

```text
                  books
                     │
         ┌───────────┴───────────┐
         ▼                       ▼

reading_plans              progress

         │                       │

         ▼                       ▼

reading_sessions       analytics

         │

         ▼

reflections

         │

         ▼

summaries

         │

   ┌─────┴────────┐

   ▼              ▼

flashcards      quizzes

         │

         ▼

vocabulary
```

---

# 8. Table Specifications

---

# Table: books

Stores all books in the user's library.

| Column      | Type         | Description          |
| ----------- | ------------ | -------------------- |
| id          | Integer (PK) | Book ID              |
| title       | String       | Book title           |
| author      | String       | Author name          |
| genre       | String       | Genre                |
| description | Text         | Book description     |
| total_pages | Integer      | Number of pages      |
| language    | String       | Language             |
| difficulty  | Enum         | Easy / Medium / Hard |
| rating      | Float        | Average rating       |
| cover_url   | String       | Cover image          |
| created_at  | Timestamp    | Added date           |

---

# Table: reading_plans

Stores AI-generated reading schedules.

| Column             | Type      |
| ------------------ | --------- |
| id                 | Integer   |
| plan_name          | String    |
| deadline           | Date      |
| daily_target_pages | Integer   |
| estimated_hours    | Float     |
| priority_order     | JSON      |
| status             | Enum      |
| created_at         | Timestamp |

---

# Table: reading_sessions

Stores every reading session.

| Column           | Type    |
| ---------------- | ------- |
| id               | Integer |
| book_id          | FK      |
| session_date     | Date    |
| pages_read       | Integer |
| duration_minutes | Integer |
| chapter          | String  |
| notes            | Text    |

---

# Table: progress

Tracks current reading progress.

| Column       | Type      |
| ------------ | --------- |
| id           | Integer   |
| book_id      | FK        |
| current_page | Integer   |
| percentage   | Float     |
| completed    | Boolean   |
| last_updated | Timestamp |

---

# Table: analytics

Stores computed analytics.

| Column           | Type    |
| ---------------- | ------- |
| id               | Integer |
| total_books      | Integer |
| completed_books  | Integer |
| total_pages      | Integer |
| reading_speed    | Float   |
| reading_streak   | Integer |
| longest_streak   | Integer |
| predicted_finish | Date    |

---

# Table: recommendations

Stores AI recommendations.

| Column              | Type      |
| ------------------- | --------- |
| id                  | Integer   |
| recommendation_type | String    |
| content             | Text      |
| confidence          | Float     |
| generated_at        | Timestamp |

---

# Table: summaries

Stores chapter summaries.

| Column     | Type      |
| ---------- | --------- |
| id         | Integer   |
| book_id    | FK        |
| chapter    | String    |
| summary    | Text      |
| created_at | Timestamp |

---

# Table: flashcards

| Column     | Type    |
| ---------- | ------- |
| id         | Integer |
| book_id    | FK      |
| question   | Text    |
| answer     | Text    |
| difficulty | Enum    |

---

# Table: quizzes

| Column   | Type    |
| -------- | ------- |
| id       | Integer |
| book_id  | FK      |
| question | Text    |
| options  | JSON    |
| answer   | String  |

---

# Table: vocabulary

| Column   | Type    |
| -------- | ------- |
| id       | Integer |
| book_id  | FK      |
| word     | String  |
| meaning  | Text    |
| example  | Text    |
| mastered | Boolean |

---

# Table: reflections

Stores user learning reflections.

| Column     | Type      |
| ---------- | --------- |
| id         | Integer   |
| book_id    | FK        |
| reflection | Text      |
| difficulty | Integer   |
| mood       | String    |
| created_at | Timestamp |

---

# Table: preferences

Stores long-term preferences.

| Column               | Type    |
| -------------------- | ------- |
| id                   | Integer |
| favorite_genre       | String  |
| reading_speed        | Float   |
| daily_reading_time   | Integer |
| preferred_difficulty | Enum    |

---

# Table: memory

Stores persistent AI memory.

| Column      | Type      |
| ----------- | --------- |
| id          | Integer   |
| memory_type | String    |
| key         | String    |
| value       | JSON      |
| updated_at  | Timestamp |

---

# 9. ChromaDB Design

ChromaDB stores semantic embeddings used by the Learning Agent.

## Collections

### books_collection

Stores:

* Entire books
* Metadata

---

### chapter_collection

Stores:

* Individual chapters
* Embeddings
* Metadata

---

### notes_collection

Stores:

* User notes
* AI notes

---

### highlights_collection

Stores:

* Highlights
* Important passages

---

## Metadata Example

```json
{
  "book": "Atomic Habits",
  "chapter": 5,
  "page": 72,
  "chunk": 14
}
```

---

# 10. Long-Term Memory Design

The AI maintains persistent preferences that improve personalization.

Stored information includes:

* Favorite genres
* Preferred reading time
* Average reading speed
* Preferred difficulty
* Common reading schedule
* Frequently revisited topics
* Learning preferences

This data is stored in the `memory` and `preferences` tables and updated after relevant interactions.

---

# 11. Session Memory Design

Session memory is maintained outside the relational database (e.g., in LangGraph state or in-memory cache).

Example session state:

```json
{
  "current_goal": "Finish 3 books this month",
  "selected_books": [
    "Clean Code",
    "Atomic Habits"
  ],
  "conversation_context": "...",
  "temporary_plan": {}
}
```

Session memory is discarded when the workflow or user session ends.

---

# 12. Data Relationships

| Parent        | Child            | Relationship |
| ------------- | ---------------- | ------------ |
| books         | reading_sessions | One-to-Many  |
| books         | progress         | One-to-One   |
| books         | summaries        | One-to-Many  |
| books         | flashcards       | One-to-Many  |
| books         | quizzes          | One-to-Many  |
| books         | vocabulary       | One-to-Many  |
| books         | reflections      | One-to-Many  |
| reading_plans | reading_sessions | One-to-Many  |

These relationships support efficient joins and maintain referential integrity.

---

# 13. Database Workflows

## Add a New Book

```text
User

↓

Books Table

↓

Metadata Retrieved

↓

Update Books Table

↓

Generate Reading Plan
```

---

## Update Reading Progress

```text
Reading Session

↓

Update Progress

↓

Update Analytics

↓

Trigger Reflection

↓

Update Reading Plan
```

---

## Upload Book

```text
PDF

↓

Filesystem

↓

Chunk

↓

Embeddings

↓

ChromaDB
```

---

## Ask Question

```text
Question

↓

Embedding

↓

ChromaDB

↓

Relevant Chunks

↓

LLM

↓

Answer
```

---

## Generate Quiz

```text
Book

↓

Retrieve Chapter

↓

LLM

↓

Store Quiz

↓

Quiz Table
```

---

# 14. Indexing Strategy

To improve query performance, create indexes on frequently searched columns.

Recommended indexes:

| Table            | Columns               |
| ---------------- | --------------------- |
| books            | title, author         |
| reading_sessions | book_id, session_date |
| progress         | book_id               |
| summaries        | book_id, chapter      |
| quizzes          | book_id               |
| flashcards       | book_id               |
| vocabulary       | word                  |
| reflections      | book_id, created_at   |
| recommendations  | generated_at          |

ChromaDB internally manages vector indexes for similarity search.

---

# 15. Constraints & Validation

### Primary Keys

Every table contains a unique integer primary key.

### Foreign Keys

Enforce relationships between books and dependent entities.

### Validation Rules

* `total_pages` > 0
* `current_page` ≤ `total_pages`
* `percentage` between 0 and 100
* `reading_speed` > 0
* `daily_reading_time` > 0
* `confidence` between 0.0 and 1.0

### Cascading Behavior

* Deleting a book should also remove associated progress, summaries, flashcards, quizzes, vocabulary, and reflections.

---

# 16. Backup & Recovery

### SQLite

* Scheduled backups of the database file.
* Transaction-based recovery for writes.
* Versioned backups before schema migrations.

### ChromaDB

* Periodic export of collections.
* Rebuild capability from original documents if required.

---

# 17. Future Scalability

The schema is designed for future expansion.

Planned improvements include:

* PostgreSQL migration.
* Multi-user support with a dedicated `users` table.
* Shared reading groups.
* Collaborative notes.
* Book collections and tags.
* Notification history.
* AI conversation history.
* Versioned reading plans.
* Advanced analytics warehouse.

The current design minimizes migration effort by maintaining normalized entities and clear relationships.

---

# 18. Summary

The database architecture of **BookPilot AI** combines the strengths of relational and vector storage. SQLite manages structured application data such as books, plans, progress, analytics, and learning artifacts, while ChromaDB enables semantic retrieval for uploaded documents and AI-assisted learning.

The schema supports adaptive planning, personalized recommendations, long-term memory, and Retrieval-Augmented Generation, providing a scalable foundation for the application's agentic workflows. By separating transactional data from vectorized knowledge, the design ensures efficient querying, maintainability, and readiness for future enhancements such as multi-user support and cloud-native deployments.
