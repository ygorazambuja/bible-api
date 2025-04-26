from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING, List
from sqlalchemy.orm import relationship as sa_relationship

if TYPE_CHECKING:
    from domain.book import Book


class Bible(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    short_name: str
    books: List["Book"] = Relationship(
        back_populates="bible",
        sa_relationship=sa_relationship("Book", back_populates="bible"),
    )
