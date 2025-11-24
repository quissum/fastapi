from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.routes.auth import router as auth_router
from app.api.routes.tasks import router as tasks_router
from app.core.config import settings
from app.db import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print('DB created!')
    yield
    print('close!')


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(tasks_router)
