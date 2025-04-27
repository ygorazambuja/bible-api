from fastapi import HTTPException, APIRouter, Query
from ..domain.bible import Bible
from ..domain.book import Book
from ..domain.verse import Verse
from typing import List, Optional
from http import HTTPStatus
from ..database.database import SessionDep
from ..services.bibles import get_bible_by_abbrev
from ..services.books import get_book_by_abbrev
from ..services.books import get_books_by_bible_abbrev
from ..services.verses import get_verses_by_book_abbrev, get_verses_by_range

router = APIRouter()


@router.get("", response_model=List[Bible])
async def get_bibles(db: SessionDep):
    bibles = get_bibles(db)
    return bibles


@router.get("/{bible_abbrev}", response_model=Bible, status_code=HTTPStatus.OK)
async def get_bible(bible_abbrev: str, db: SessionDep):
    bible = get_bible_by_abbrev(db, bible_abbrev.upper())

    if not bible:
        raise HTTPException(
            status_code=404, detail=f"Bible with abbreviation {bible_abbrev} not found"
        )

    return bible


@router.get("/{bible_abbrev}/books", response_model=List[Book])
async def get_books(bible_abbrev: str, db: SessionDep):
    bible = get_bible_by_abbrev(db, bible_abbrev.upper())

    if not bible:
        raise HTTPException(
            status_code=404, detail=f"Bible with abbreviation {bible_abbrev} not found"
        )

    books = get_books_by_bible_abbrev(db, bible_abbrev.upper())
    return books


@router.get("/{bible_abbrev}/books/{book_abbrev}", response_model=Book)
async def get_book(bible_abbrev: str, book_abbrev: str, db: SessionDep):
    bible = get_bible_by_abbrev(db, bible_abbrev.upper())

    if not bible:
        raise HTTPException(
            status_code=404, detail=f"Bible with abbreviation {bible_abbrev} not found"
        )

    book = get_book_by_abbrev(db, book_abbrev.upper())
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
    bible = get_bible_by_abbrev(db, bible_abbrev.upper())

    if not bible:
        raise HTTPException(
            status_code=404, detail=f"Bible with abbreviation {bible_abbrev} not found"
        )

    book = get_book_by_abbrev(db, book_abbrev.upper())
    if not book:
        raise HTTPException(
            status_code=404, detail=f"Book with abbreviation {book_abbrev} not found"
        )

    verses = get_verses_by_book_abbrev(db, book_abbrev.upper(), chapter, verse)
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
    bible = get_bible_by_abbrev(db, bible_abbrev)

    if not bible:
        raise HTTPException(
            status_code=404, detail=f"Bible with abbreviation {bible_abbrev} not found"
        )

    book = get_book_by_abbrev(db, book_abbrev.upper())

    if not book or not book.id:
        raise HTTPException(
            status_code=404, detail=f"Book with abbreviation {book_abbrev} not found"
        )

    from_verse = from_verse or 1
    to_verse = to_verse or 1000

    return get_verses_by_range(db, book.id, chapter, from_verse, to_verse)
