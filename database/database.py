from sqlmodel import Session, SQLModel, create_engine
from fastapi import Depends
from typing import Annotated

DATABASE_URL = "sqlite:///bible.db"
engine = create_engine(DATABASE_URL)


async def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


SessionDep = Annotated[Session, Depends(get_session)]


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
