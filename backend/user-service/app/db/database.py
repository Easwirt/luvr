import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.config import POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_USER
from typing import AsyncGenerator

POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

Base = declarative_base()

class PostgreDB:
    def __init__(self):
        self.database_url = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
        self.engine = create_async_engine(self.database_url, echo=True, pool_size=10, max_overflow=20)
        self.session_factory = async_sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session

postgreDB = PostgreDB()

engine = postgreDB.engine

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with postgreDB.session_factory() as session:
        yield session
