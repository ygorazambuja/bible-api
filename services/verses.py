from ..database.database import SessionDep
from ..domain.verse import Verse
from .books import get_book_by_abbrev
from sqlmodel import select


def get_verses_by_book_abbrev(
    db: SessionDep,
    book_abbrev: str,
    chapter: int | None = None,
    verse: int | None = None,
) -> list[Verse]:
    book = get_book_by_abbrev(db, book_abbrev)

    if not book or not book.id:
        raise Exception(f"Book with abbreviation {book_abbrev} not found")

    if chapter is None and verse is None:
        return get_verses_by_book_id(db, book.id)

    if chapter is not None and verse is None:
        return get_verses_by_book_id(db, book.id, chapter)

    return get_verses_by_book_id(db, book.id, chapter, verse)


def get_verses_by_book_id(
    db: SessionDep, book_id: int, chapter: int | None = None, verse: int | None = None
) -> list[Verse]:
    query = select(Verse).where(Verse.book_id == book_id)

    if chapter is not None:
        query = query.where(Verse.chapter == chapter)

    if verse is not None:
        query = query.where(Verse.verse == verse)

    verses = db.exec(query).all()

    if not verses:
        raise Exception(f"No verses found for book with id {book_id}")

    return list(verses)


def get_verses_by_range(
    db: SessionDep, book_id: int, chapter: int, from_verse: int, to_verse: int
) -> list[Verse]:
    verses = db.exec(
        select(Verse).where(
            Verse.book_id == book_id,
            Verse.chapter == chapter,
            Verse.verse >= from_verse,
            Verse.verse <= to_verse,
        )
    ).all()

    if not verses:
        raise Exception(f"No verses found for book with id {book_id}")

    return list(verses)
