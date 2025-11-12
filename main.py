from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_tables, delete_tables
from router import router as task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await delete_tables()
    # print('DB cleared!')
    await create_tables()
    print('DB created!')
    yield
    print('close!')


app = FastAPI(lifespan=lifespan)
app.include_router(task_router)
