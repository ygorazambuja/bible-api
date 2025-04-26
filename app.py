from fastapi import FastAPI
from contextlib import asynccontextmanager
try:
    from database.database import create_db_and_tables
    from routers import bibles
except ImportError:
    # Try relative imports if absolute imports fail
    from .database.database import create_db_and_tables
    from .routers import bibles


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Bible API", lifespan=lifespan)

app.include_router(bibles.router, prefix="/bibles", tags=["bibles"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 