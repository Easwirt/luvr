from fastapi import FastAPI
from app.db.database import Base, postgreDB
from app.api.endpoints.user import router
import py_eureka_client.eureka_client as eureka_client
from app.config import EUREKA_CLIENT_SERVICEURL_DEFAULTZONE
from contextlib import asynccontextmanager

EUREKA_SERVER = EUREKA_CLIENT_SERVICEURL_DEFAULTZONE
SERVICE_NAME = "user-service"
SERVICE_PORT = 8000

async def init_eureka():
    await eureka_client.init_async(
        eureka_server=EUREKA_SERVER,
        app_name=SERVICE_NAME,
        instance_port=SERVICE_PORT,
        renewal_interval_in_secs=30,
        duration_in_secs=90,
    )

async def create_db():
    async with postgreDB.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    await init_eureka()
    yield
    print("Shutting down the application...")

app = FastAPI(lifespan=lifespan)

app.include_router(router)
