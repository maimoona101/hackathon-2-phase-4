from sqlmodel import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from ..core.config import settings

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=300
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_session() -> Generator:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
