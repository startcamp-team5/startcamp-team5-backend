from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.core.init_db import initialize_database

from app.locations.router import router as locations_router
from app.posts.router import router as posts_router
from app.comments.router import router as comments_router

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("==============================")
    print("Application startup")
    print("==============================")

    initialize_database()

    yield

    print("==============================")
    print("Application shutdown")
    print("==============================")
  
app = FastAPI(
    title="LocalHub API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(
    locations_router,
    prefix="/api",
)

app.include_router(
    posts_router,
    prefix="/api",
)
app.include_router(
    comments_router,
    prefix="/api"
)

# 배포된 이후 CORS 정책을 허용하기 위해 아래 설정 추가
app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "*"
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ],
)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
    }