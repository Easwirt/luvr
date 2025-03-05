from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import Base, postgreDB
from app.api.endpoints.user import router
from sqlalchemy.future import select
import py_eureka_client.eureka_client as eureka_client


app = FastAPI()

EUREKA_SERVER = "http://localhost:8761/eureka/"  # Адрес Eureka Server
SERVICE_NAME = "fastapi-service"
SERVICE_PORT = 8000

eureka_client.init(
    eureka_server=EUREKA_SERVER,
    app_name=SERVICE_NAME,
    instance_port=SERVICE_PORT
)

async def init_eureka():
    await eureka_client.init_async(
        eureka_server=EUREKA_SERVER,
        app_name=SERVICE_NAME,
        instance_port=SERVICE_PORT
    )

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
