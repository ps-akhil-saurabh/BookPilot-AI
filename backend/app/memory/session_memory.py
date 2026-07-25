"""
BookPilot AI — Session Memory Module

Maintains in-memory conversational state and current request context.
"""

from typing import List, Dict, Any
from app.core.config import settings

class SessionMemoryManager:
    """Manages short-term conversation context in memory."""

    def __init__(self):
        self.sessions: Dict[str, List[Dict[str, str]]] = {}

    def add_message(self, session_id: str, role: str, content: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        
        self.sessions[session_id].append({"role": role, "content": content})
        
        # Prune if exceeding max messages
        if len(self.sessions[session_id]) > settings.MAX_SESSION_MESSAGES:
            self.sessions[session_id] = self.sessions[session_id][-settings.MAX_SESSION_MESSAGES:]

    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        return self.sessions.get(session_id, [])

    def clear_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

session_memory = SessionMemoryManager()
