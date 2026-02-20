from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid


class SessionBase(SQLModel):
    user_id: uuid.UUID
    token: str = Field(unique=True, nullable=False)
    expires_at: datetime


class Session(SessionBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)