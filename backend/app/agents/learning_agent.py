"""
BookPilot AI — Learning Agent

Generates explanations, summaries, quizzes, flashcards, and vocabulary using RAG + Llama.
"""

from typing import Dict, Any, Optional
from app.rag.retrieval import retrieve_relevant_chunks
from app.memory.summarizer import get_llm
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.logger import get_agent_logger

logger = get_agent_logger("LearningAgent")

class LearningAgent:
    """Learning Agent: Answers questions and generates study materials."""

    async def answer_question(self, question: str, book_id: Optional[int] = None) -> Dict[str, Any]:
        logger.info(f"LearningAgent: Answering question '{question}' (Book ID: {book_id})")

        # Step 1: Retrieve context
        chunks = retrieve_relevant_chunks(question, book_id=book_id)
        
        context_str = "\n\n".join([c["text"] for c in chunks]) if chunks else "No specific book content found."
        
        # Step 2: Prompt LLM
        llm = get_llm()
        messages = [
            SystemMessage(content=(
                "You are BookPilot AI, a knowledgeable and encouraging Reading Mentor. "
                "Answer the user's question clearly, grounded in the provided context if available."
            )),
            HumanMessage(content=f"Context from book:\n{context_str}\n\nUser Question: {question}"),
        ]

        response = await llm.ainvoke(messages)
        
        return {
            "answer": response.content.strip(),
            "sources": [c["metadata"].get("chunk_index", 0) for c in chunks],
            "grounded": len(chunks) > 0,
        }

    async def generate_summary(self, text_or_context: str) -> Dict[str, Any]:
        logger.info("LearningAgent: Generating summary")
        llm = get_llm()
        messages = [
            SystemMessage(content="You are an expert reading mentor. Summarize the text into key points and a brief overview."),
            HumanMessage(content=f"Text to summarize:\n{text_or_context}"),
        ]
        response = await llm.ainvoke(messages)
        return {"summary": response.content.strip()}

learning_agent = LearningAgent()
