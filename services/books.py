from ..database.database import SessionDep
from ..domain.book import Book
from sqlmodel import func, select
from .bibles import get_bible_by_abbrev


def get_book_by_abbrev(db: SessionDep, book_abbrev: str) -> Book | None:
    book = db.exec(
        select(Book).where(func.upper(Book.short_name) == book_abbrev.upper())
    ).first()
    return book


def get_books_by_bible_id(db: SessionDep, bible_id: int) -> list[Book]:
    books = db.exec(select(Book).where(Book.bible_id == bible_id)).all()

    if not books:
        raise Exception(f"No books found for bible with id {bible_id}")

    return list(books)


def get_books_by_bible_abbrev(db: SessionDep, bible_abbrev: str) -> list[Book]:
    bible = get_bible_by_abbrev(db, bible_abbrev)

    if not bible or not bible.id:
        raise Exception(f"Bible with abbreviation {bible_abbrev} not found")

    return get_books_by_bible_id(db, bible.id)


def get_book_by_bible_abbrev_and_book_abbrev(
    db: SessionDep, bible_abbrev: str, book_abbrev: str
) -> Book | None:
    bible = get_bible_by_abbrev(db, bible_abbrev)

    if not bible or not bible.id:
        raise Exception(f"Bible with abbreviation {bible_abbrev} not found")

    book = db.exec(
        select(Book).where(
            Book.bible_id == bible.id,
            func.upper(Book.short_name) == book_abbrev.upper(),
        )
    ).first()

    if not book:
        raise Exception(
            f"Book with abbreviation {book_abbrev} not found in bible with abbreviation {bible_abbrev}"
        )

    return book
