from ..database.database import SessionDep
from ..domain.bible import Bible
from sqlmodel import func, select


def get_bible_by_abbrev(db: SessionDep, bible_abbrev: str) -> Bible | None:
    bible = db.exec(
        select(Bible).where(func.upper(Bible.short_name) == bible_abbrev.upper())
    ).first()

    if not bible:
        raise Exception(f"Bible with abbreviation {bible_abbrev} not found")

    return bible
