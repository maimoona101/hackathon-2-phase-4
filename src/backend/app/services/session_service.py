"""
Session Service for the AI-powered Todo Chatbot
"""

from sqlmodel import Session, select
from typing import Optional
from datetime import datetime, timedelta
import uuid

from ..models.user_session import UserSession, UserSessionCreate


class SessionService:
    def __init__(self, session: Session):
        self.session = session

    def create_user_session(self, user_id: int, session_token: str, expires_in_hours: int = 24) -> UserSession:
        """Create a new user session"""
        expires_at = datetime.utcnow() + timedelta(hours=expires_in_hours)
        user_session = UserSession(
            user_id=user_id,
            session_token=session_token,
            expires_at=expires_at
        )
        self.session.add(user_session)
        self.session.commit()
        self.session.refresh(user_session)
        return user_session

    def get_active_session_by_token(self, session_token: str) -> Optional[UserSession]:
        """Get an active session by token"""
        statement = select(UserSession).where(
            UserSession.session_token == session_token,
            UserSession.expires_at > datetime.utcnow()
        )
        return self.session.exec(statement).first()

    def get_session_by_id(self, session_id: str) -> Optional[UserSession]:
        """Get a session by ID"""
        statement = select(UserSession).where(UserSession.id == session_id)
        return self.session.exec(statement).first()

    def invalidate_session(self, session_id: str) -> bool:
        """Invalidate a session by setting its expiration to now"""
        user_session = self.get_session_by_id(session_id)
        if user_session:
            user_session.expires_at = datetime.utcnow()
            self.session.add(user_session)
            self.session.commit()
            return True
        return False

    def cleanup_expired_sessions(self) -> int:
        """Remove expired sessions and return count of deleted sessions"""
        statement = select(UserSession).where(UserSession.expires_at <= datetime.utcnow())
        expired_sessions = self.session.exec(statement).all()

        for session in expired_sessions:
            self.session.delete(session)

        self.session.commit()
        return len(expired_sessions)