from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import Base, postgreDB
from app.api.endpoints.user import router
from sqlalchemy.future import select

app = FastAPI()

# Ensure that the database tables are created asynchronously
async def create_db():
    async with postgreDB.engine.begin() as conn:
        # Create all tables (this works asynchronously)
        await conn.run_sync(Base.metadata.create_all)

# Run this method when the application starts
@app.on_event("startup")
async def startup():
    await create_db()

# Include the user router
app.include_router(router)
