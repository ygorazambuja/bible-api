from sqlmodel import Session
import json
from domain.bible import Bible
from domain.book import Book
from domain.verse import Verse
from database.database import engine, create_db_and_tables

# Create tables if they don't exist
create_db_and_tables()

with Session(engine) as session:
    biblies = {
        "NAA": {"name": "Nova Almeida Atualizada", "short_name": "NAA"},
        "NTLH": {"name": "Nova Tradução Literal Hebraica", "short_name": "NTLH"},
        "ACF": {"name": "Almeida Corrigida Fiel", "short_name": "ACF"},
        "ARA": {"name": "Almeida Revista e Atualizada", "short_name": "ARA"},
        "AS21": {"name": "Almeida Revista e Atualizada 2021", "short_name": "AS21"},
        "JFAA": {"name": "João Ferreira de Almeida Atualizada", "short_name": "JFAA"},
        "KJA": {"name": "King James Atualizada", "short_name": "KJA"},
        "KJF": {"name": "King James Fiel", "short_name": "KJF"},
        "NBV": {"name": "Nova Biblia Viva", "short_name": "NBV"},
        "NVI": {"name": "Nova Versão Internacional", "short_name": "NVI"},
        "NVT": {"name": "Nova Versão Transformadora", "short_name": "NVT"},
        "TB": {"name": "Tradução Brasileira", "short_name": "TB"},
    }

    for bible_name, bible_data in biblies.items():
        with open(f"raw_data/{bible_name}.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            bible = Bible(name=bible_data["name"], short_name=bible_data["short_name"])
            session.add(bible)
            session.flush()

        assert bible.id is not None, "Bible ID should be assigned after flush"

        for i, b in enumerate(data):
            book = Book(
                name=b["name"], short_name=b["abbrev"], number=i + 1, bible_id=bible.id
            )
            session.add(book)
            session.flush()

            assert book.id is not None, "Book ID should be assigned after flush"

            for j, c in enumerate(b["chapters"]):
                for k, v in enumerate(c):
                    verse = Verse(book_id=book.id, chapter=j + 1, verse=k + 1, text=v)
                    session.add(verse)

        session.commit()
