"""
Runner for the Gemini Agent
Manages conversations and interactions with the AI assistant
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from sqlmodel import Session

from .gemini_agent import gemini_todo_agent
from .gemini_runner import gemini_agent_runner

load_dotenv()

class AgentRunner:
    def __init__(self):
        self.agent = gemini_todo_agent

    async def process_conversation(self, user_message: str, session: Session, user_id: str = None):
        """Process a complete conversation turn with Gemini"""
        # Delegate to the Gemini agent runner
        return await gemini_agent_runner.process_conversation(user_message, session, user_id)

# Global instance
agent_runner = AgentRunner()