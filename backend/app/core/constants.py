"""
BookPilot AI — Application Constants

Centralized constants used across the application.
No hardcoded values should exist outside this module.
"""


# ── Reading Difficulty ───────────────────────────────────────────
class Difficulty:
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    ALL = [EASY, MEDIUM, HARD]


# ── Reading Plan Status ──────────────────────────────────────────
class PlanStatus:
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    ALL = [ACTIVE, COMPLETED, PAUSED, CANCELLED]


# ── Agent Types ──────────────────────────────────────────────────
class AgentType:
    PLANNER = "planner"
    METADATA = "metadata"
    SCHEDULING = "scheduling"
    LEARNING = "learning"
    RECOMMENDATION = "recommendation"
    ANALYTICS = "analytics"
    REFLECTION = "reflection"
    ALL = [PLANNER, METADATA, SCHEDULING, LEARNING, RECOMMENDATION, ANALYTICS, REFLECTION]


# ── Intent Types (Planner Agent output) ──────────────────────────
class IntentType:
    READING_PLAN = "reading_plan"
    EXPLAIN = "explain"
    SUMMARIZE = "summarize"
    QUIZ = "quiz"
    FLASHCARD = "flashcard"
    VOCABULARY = "vocabulary"
    RECOMMENDATION = "recommendation"
    ANALYTICS = "analytics"
    PROGRESS_UPDATE = "progress_update"
    REPLAN = "replan"
    GENERAL = "general"


# ── MCP Tool Types ───────────────────────────────────────────────
class MCPType:
    BROWSER = "browser"
    CALENDAR = "calendar"
    FILESYSTEM = "filesystem"
    DATABASE = "database"
    ALL = [BROWSER, CALENDAR, FILESYSTEM, DATABASE]


# ── Reflection Status ────────────────────────────────────────────
class ReflectionStatus:
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"


# ── Workflow Status ──────────────────────────────────────────────
class WorkflowStatus:
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    WAITING = "waiting"


# ── Quiz Types ───────────────────────────────────────────────────
class QuizType:
    MCQ = "mcq"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    ALL = [MCQ, TRUE_FALSE, SHORT_ANSWER]


# ── Recommendation Types ─────────────────────────────────────────
class RecommendationType:
    BOOK = "book"
    READING_ORDER = "reading_order"
    MOOD_BASED = "mood_based"
    GENRE = "genre"


# ── Memory Types ─────────────────────────────────────────────────
class MemoryType:
    PREFERENCE = "preference"
    HABIT = "habit"
    INSIGHT = "insight"
    CONVERSATION = "conversation"


# ── Default Values ───────────────────────────────────────────────
DEFAULT_READING_SPEED_PPH = 25.0  # pages per hour
DEFAULT_DAILY_READING_MINUTES = 30
DEFAULT_PAGES_PER_MINUTE = 0.42  # ~25 pages/hour

# Difficulty affects estimated reading time
DIFFICULTY_MULTIPLIERS = {
    Difficulty.EASY: 1.0,
    Difficulty.MEDIUM: 1.3,
    Difficulty.HARD: 1.7,
}

# Maximum number of books per plan
MAX_BOOKS_PER_PLAN = 20

# Supported file formats
SUPPORTED_FORMATS = ["pdf", "epub", "md"]
