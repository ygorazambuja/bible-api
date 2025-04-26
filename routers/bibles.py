from fastapi import HTTPException, APIRouter, Query
from sqlmodel import select
from ..domain.bible import Bible
from ..domain.book import Book
from ..domain.verse import Verse
from typing import List, Optional
from sqlalchemy import func
from http import HTTPStatus
from ..database.database import SessionDep

router = APIRouter()


@router.get("", response_model=List[Bible])
async def get_bibles(db: SessionDep):
    bibles = db.exec(select(Bible)).all()
    return bibles


@router.get("/{bible_abbrev}", response_model=Bible, status_code=HTTPStatus.OK)
async def get_bible(bible_abbrev: str, db: SessionDep):
    bible = db.exec(
        select(Bible).where(Bible.short_name == bible_abbrev.upper())
    ).first()

    if not bible:
        raise HTTPException(
            status_code=404, detail=f"Bible with abbreviation {bible_abbrev} not found"
        )

    books = db.exec(select(Book).where(Book.bible_id == bible.id)).all()

    result = {
        "id": bible.id,
        "name": bible.name,
        "short_name": bible.short_name,
        "books": [],
    }

    for book in books:
        book_data = {
            "id": book.id,
            "name": book.name,
            "number": book.number,
            "short_name": book.short_name,
        }
        result["books"].append(book_data)

    return result


@router.get("/{bible_abbrev}/books/{book_abbrev}", response_model=Book)
async def get_book(bible_abbrev: str, book_abbrev: str, db: SessionDep):
    bible = db.exec(
        select(Bible).where(Bible.short_name == bible_abbrev.upper())
    ).first()

    if not bible:
        raise HTTPException(
            status_code=404, detail=f"Bible with abbreviation {bible_abbrev} not found"
        )

    book = db.exec(
        select(Book).where(
            func.upper(Book.short_name) == book_abbrev.upper(),
            Book.bible_id == bible.id,
        )
    ).first()
    if not book:
        raise HTTPException(
            status_code=404, detail=f"Book with abbreviation {book_abbrev} not found"
        )
    return book


@router.get(
    "/{bible_abbrev}/books/{book_abbrev}/verses",
    response_model=List[Verse],
)
async def get_book_verses(
    bible_abbrev: str,
    book_abbrev: str,
    db: SessionDep,
    chapter: Optional[int] = Query(None, description="Filter by chapter number"),
    verse: Optional[int] = Query(None, description="Filter by verse number"),
):
    bible = db.exec(
        select(Bible).where(Bible.short_name == bible_abbrev.upper())
    ).first()
    if not bible:
        raise HTTPException(
            status_code=404, detail=f"Bible with abbreviation {bible_abbrev} not found"
        )

    book = db.exec(
        select(Book).where(
            func.upper(Book.short_name) == book_abbrev.upper(),
            Book.bible_id == bible.id,
        )
    ).first()
    if not book:
        raise HTTPException(
            status_code=404, detail=f"Book with abbreviation {book_abbrev} not found"
        )

    verses = db.exec(
        select(Verse).where(
            Verse.book_id == book.id, Verse.chapter == chapter, Verse.verse == verse
        )
    ).all()
    return verses


@router.get(
    "/{bible_abbrev}/books/{book_abbrev}/chapters/{chapter}",
    response_model=List[Verse],
)
async def get_book_chapter(
    bible_abbrev: str,
    book_abbrev: str,
    chapter: int,
    db: SessionDep,
    from_verse: Optional[int] = Query(None, description="Filter by verse number"),
    to_verse: Optional[int] = Query(None, description="Filter by verse number"),
):
    bible = db.exec(
        select(Bible).where(Bible.short_name == bible_abbrev.upper())
    ).first()

    if not bible:
        raise HTTPException(
            status_code=404, detail=f"Bible with abbreviation {bible_abbrev} not found"
        )

    book = db.exec(
        select(Book).where(
            func.upper(Book.short_name) == book_abbrev.upper(),
            Book.bible_id == bible.id,
        )
    ).first()

    if not book:
        raise HTTPException(
            status_code=404, detail=f"Book with abbreviation {book_abbrev} not found"
        )

    from_verse = from_verse or 1
    to_verse = to_verse or 1000

    return db.exec(
        select(Verse).where(
            Verse.book_id == book.id,
            Verse.chapter == chapter,
            Verse.verse >= from_verse,
            Verse.verse <= to_verse,
        )
    ).all()
