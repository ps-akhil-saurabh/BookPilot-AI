"""
BookPilot AI — Summarizer Module

Summarizes long conversations or document chunks using the cloud Llama API.
"""

from app.core.config import settings
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.logger import logger

def get_llm():
    """Initialize OpenAI-compatible ChatOpenAI client pointing to cloud Llama provider."""
    return ChatOpenAI(
        model=settings.LLM_MODEL_NAME,
        openai_api_key=settings.LLM_API_KEY or "placeholder-key",
        openai_api_base=settings.LLM_BASE_URL,
        temperature=settings.LLM_TEMPERATURE,
        max_tokens=settings.LLM_MAX_TOKENS,
    )

async def summarize_text(text: str, max_words: int = 150) -> str:
    """Generate a concise summary of text using Llama."""
    try:
        llm = get_llm()
        messages = [
            SystemMessage(content=f"You are a helpful AI reading mentor. Provide a clear summary in under {max_words} words."),
            HumanMessage(content=f"Summarize the following content:\n\n{text}"),
        ]
        response = await llm.ainvoke(messages)
        return response.content.strip()
    except Exception as e:
        logger.error(f"Summarizer error: {e}")
        return text[:500] + "..." if len(text) > 500 else text
