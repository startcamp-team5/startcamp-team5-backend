from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.init_db import create_tables
from app.posts.router import router as posts_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="LocalHub API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(
    posts_router,
    prefix="/api",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}