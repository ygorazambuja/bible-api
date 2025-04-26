from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database.database import create_db_and_tables
from .routers import bibles


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Bible API", lifespan=lifespan)

app.include_router(bibles.router, prefix="/bibles", tags=["bibles"])

