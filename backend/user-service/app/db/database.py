import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.config import POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_USER
from typing import AsyncGenerator

# Get environment variables
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")  # Default PostgreSQL port

Base = declarative_base()

class PostgreDB:
    def __init__(self):
        self.database_url = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
        # Create the async engine
        self.engine = create_async_engine(self.database_url, echo=True, pool_size=10, max_overflow=20)
        # Create a session factory
        self.session_factory = async_sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session

# Initialize PostgreDB instance
postgreDB = PostgreDB()

# Export the engine for use elsewhere
engine = postgreDB.engine

# Function for getting database session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with postgreDB.session_factory() as session:
        yield session
