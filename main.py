from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database.database import create_db_and_tables
from .routers import bibles
from scalar_fastapi import get_scalar_api_reference
from .routers import ai

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Bible API", lifespan=lifespan)

app.include_router(bibles.router, prefix="/bibles", tags=["bibles"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])


@app.get("/scalar", include_in_schema=False)
async def scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url or "",
        title=app.title,
    )
