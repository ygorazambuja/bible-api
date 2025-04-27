from sqlmodel import Session, SQLModel, create_engine
from fastapi import Depends
from typing import Annotated
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/bibledb")

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)


async def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


SessionDep = Annotated[Session, Depends(get_session)]


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
