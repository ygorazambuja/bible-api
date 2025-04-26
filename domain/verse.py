from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from .book import Book


class Verse(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="book.id")
    book: Book = Relationship(back_populates="verses")
    chapter: int
    verse: int
    text: str
