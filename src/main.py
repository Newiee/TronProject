from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database.database import engine, Base
from src.routers.wallet_routers import router as tron_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(
    title="Tron Microservice",
    description="API для работы с данными сети Tron",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(tron_router, prefix="/api/v1", tags=["tron"])