import os
from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file!")

# Import your models
from .conversation import Conversation
from .message import Message

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create tables
def create_tables():
    print("Creating AI tables: Conversation and Message...")
    SQLModel.metadata.create_all(engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()
