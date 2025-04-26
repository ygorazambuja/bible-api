from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING, List
from sqlalchemy.orm import relationship as sa_relationship

if TYPE_CHECKING:
    from domain.bible import Bible
    from domain.verse import Verse


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    number: int
    short_name: str
    bible_id: int = Field(foreign_key="bible.id")
    bible: "Bible" = Relationship(
        back_populates="books",
        sa_relationship=sa_relationship("Bible", back_populates="books"),
    )
    verses: List["Verse"] = Relationship(
        back_populates="book",
        sa_relationship=sa_relationship("Verse", back_populates="book"),
    )
